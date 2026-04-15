---
title: "Cache effects in object-oriented code: computer architecture meets programming"
subtitle: "A simple demonstration revealed five layers of computer science & engineering abstraction fighting each other"
date: 2026-02-10
slug: cache-effects-in-object-oriented
canonical_url: "https://www.avikde.me/p/cache-effects-in-object-oriented"
topic: "Cache Effects In Object Oriented Programming"
concepts:
  - "Control Systems"
  - "Hardware Acceleration"
  - "Object-Oriented Design"
  - "Design Optimization"
source: Substack
author: Avik De
---

# Cache effects in object-oriented code: computer architecture meets programming

![](https://substackcdn.com/image/fetch/$s_!p-27!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2e89b29-bc5a-4d7c-8d47-a50a93e8ec02_732x755.jpeg)

*A simple demonstration revealed five layers of computer science & engineering abstraction fighting each other*

> Originally published: [2026-02-10](https://www.avikde.me/p/cache-effects-in-object-oriented)

**Topic:** [[topics/cache-effects-in-object-oriented-programming|Cache Effects In Object Oriented Programming]]
**Concepts:** [[concepts/control-systems|Control Systems]] · [[concepts/hardware-acceleration|Hardware Acceleration]] · [[concepts/object-oriented-design|Object-Oriented Design]] · [[concepts/design-optimization|Design Optimization]]
**Citations:** [[citations/youtube-com|youtube.com]] · [[citations/wccftech-com|wccftech.com]] · [[citations/pointclouds-org|pointclouds.org]] · [[citations/docs-unity3d-com|docs.unity3d.com]] · [[citations/cowboyprogramming-com|cowboyprogramming.com]] · [[citations/github-com|github.com]] · [[citations/godbolt-org|godbolt.org]] · [[citations/mlsysbook-ai|mlsysbook.ai]] · [[citations/unity-com|unity.com]] · [[citations/dev-epicgames-com|dev.epicgames.com]] · [[citations/youtu-be|youtu.be]] · [[citations/abseil-io|abseil.io]] · [[citations/en-wikipedia-org|en.wikipedia.org]]

---

Having worked in robotics research and industry for over a decade, I’ve debugged enough real-time control loops to know that the programming language abstraction can be misleading. We write object-oriented code because it’s maintainable, composable, and maps cleanly to our mental models. A robot has limbs, limbs have joints, joints have positions and velocities, so we should create a hierarchy of objects accordingly, right?

When battery life is crucial, and when microseconds matter to ensure control loops remain stable, the hardware doesn’t care about elegant class hierarchy or beautiful code. The end-product of programming is [data transformation](<https://www.youtube.com/watch?v=fHNmRkzxHWs>), and not the code itself.

This post, written with my friend  (software engineer and CS lecturer), started as a simple teaching example about Array-of-Structures vs Structure-of-Arrays (AoS vs. SoA) layouts. We thought we’d show a clean and universal performance curve demonstrating cache effects tied to C++ code.

[![](https://substackcdn.com/image/fetch/$s_!p-27!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2e89b29-bc5a-4d7c-8d47-a50a93e8ec02_732x755.jpeg)](<https://substackcdn.com/image/fetch/$s_!p-27!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2e89b29-bc5a-4d7c-8d47-a50a93e8ec02_732x755.jpeg>)Different memory hierarchy levels one of the CPU 2 cores would access (excluding the system-level; L1 is inside the core). [Original image source](<https://wccftech.com/a16-bionic-die-shot-details/>).

We built what seemed like a straightforward benchmark: measure access time for different memory strides. What we didn’t anticipate was encountering five distinct issues spanning multiple abstraction layers—from compiler behavior to microarchitecture to hardware characteristics:

  1. The compiler deleted our measurement code and unpredictably stored variables in memory vs. registers

  2. The CPU’s pipeline hazards dominated our memory access time

  3. The CPU’s dynamic frequency scaling skewed our results

  4. The hardware prefetcher made our predictions wrong

  5. Different processors gave wildly different results




This illustrates the gap between abstraction and performance. Programming languages provide abstraction above the hardware, but achieving good performance requires understanding how code executes on the underlying architecture. While some of our issues may be familiar to experienced programmers, others might be surprising even to veterans.

Thanks for reading min{power}! Subscribe for free to receive new posts and support my work.

### Four examples showing why you should care

There are many real-world examples using an "array of structures" organization for good reasons: it's faster to prototype, easier to reason about when objects manage their own state, and typically more readable for developers.

**Example 1: PCL (Point Cloud Library)**[PointXYZRGB](<https://pointclouds.org/documentation/point__types_8hpp_source.html>) structure.

[![](https://substackcdn.com/image/fetch/$s_!ckiW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf47b546-6854-4917-bc18-d35443322840_2184x752.png)](<https://substackcdn.com/image/fetch/$s_!ckiW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf47b546-6854-4917-bc18-d35443322840_2184x752.png>)

When you have `pcl::PointCloud<PointXYZRGB>` with millions of points, the memory layout looks like
    
    
    [x0, y0, z0, pad, rgb0, x1, y1, z1, pad, rgb1, ...]

For an example task of filtering by distance (operating on the xyz only), we get 40% extra cache misses. For a color segmentation task operating on rgb only, 4x extra cache misses.

**Example 2: Unity[GameObject-Component System](<https://docs.unity3d.com/510/Documentation/Manual/TheGameObject-ComponentRelationship.html>)**. GameObjects directly contain Component instances by value, e.g. a GameObject with Transform, Rigidbody, and Collider components stored as member data. This is classic AoS: each GameObject owns its component data, providing flexible composition but poor cache locality when iterating over many objects.

**Example 3: Box2D (version 2.x).** Each b2Body contains position, velocity, and force data as members (e.g. `b2Vec2 m_linearVelocity`). Most traditional object-oriented game engines before the [ECS trend](<https://cowboyprogramming.com/2007/01/05/evolve-your-heirachy/>) used composition with value semantics—each enemy/player/NPC object contained all its data directly. However, Box2D v3.0 (2024) moved away from this, now using handle-based IDs and storing body data separately for better performance.

**Example 4: Humanoid joints.** Last but not least, here is a practical example of a humanoid robot joint that should be quite relatable:

[![](https://substackcdn.com/image/fetch/$s_!_KTd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd56c5d91-ce71-44ab-a05a-e86208a295ad_2184x932.png)](<https://substackcdn.com/image/fetch/$s_!_KTd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd56c5d91-ce71-44ab-a05a-e86208a295ad_2184x932.png>)

A Limb would be composed of Joints, with Joint specialized into different joint types.

Suppose the humanoid robot has 50 joints. Computing Jacobians requires accessing each joint’s position: 5.5kB loaded into cache (87 cache misses), when we only need 200 bytes (4 cache misses if organized as an array of positions).

Now that we have shown that this organization occurs commonly, we will dig in and try to measure the effect it has.

### An even simpler example to dig into

We created an even simpler example with a single data array and a parameterized “stride” for a strided access pattern. This would occur in the example above with `stride = sizeof(Joint)`. Our goal was to time how long it takes to access a fixed number of elements with different strides, as in the code below.

_The actual code for replicating all these measurements, and more, is[on github](<https://github.com/avikde/caching-tester>): feel free to try it out._

[![](https://substackcdn.com/image/fetch/$s_!avv2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8b0a4048-5617-4744-acb9-4b835a43b592_2296x2192.png)](<https://substackcdn.com/image/fetch/$s_!avv2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8b0a4048-5617-4744-acb9-4b835a43b592_2296x2192.png>)

**What we expect to see:** Effectively, as we access data, the processor can load a segment from main memory into cache, in blocks. 
    
    
    Data:    |x| | | | |x| |...
              ← stride →
    Cache:   |y|y|y|y|y|y|y|y|z|z|...
              ← line size  →

As stride increases, visiting the same number of elements requires caching more blocks. If memory movement dominates, we expect a linear rise in time as stride increases and more cache lines are touched. (More on what happens after each access hits a separate cache line below.)

Understanding the results from this "simple" example felt like peeling endless layers of an onion, but was very gratifying at the same time!

Thanks for reading min{power}! Subscribe for free to receive new posts and support my work.

#### Issue 1: Controlling compiler optimizations

With the code snipped above, the [assembler output](<https://godbolt.org/z/bxdMzcn4c>) showed:
    
    
    testStride(unsigned long):
            ret
    data:
            .zero   256000000

Of course! `sink` was being optimized out, and my firmware programming background caused me to add a volatile to its declaration. However, something in the asm output for the loop looked amiss. Can you spot it?

[![](https://substackcdn.com/image/fetch/$s_!HWZZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb40ac46-901f-409f-9694-82ecb41de011_2404x1112.png)](<https://substackcdn.com/image/fetch/$s_!HWZZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb40ac46-901f-409f-9694-82ecb41de011_2404x1112.png>)

While data should be loaded from memory to a register, sink should be able to remain in a register. However, volatile forces it to be loaded and stored because the compiler must assume that it can be modified externally. So we get rid of volatile, and uncomment the last line:
    
    
    if (sink == -1.0f) std::cout << "";

The new loop looks like

[![](https://substackcdn.com/image/fetch/$s_!DZpq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8d29b301-f48d-4272-ab5e-d36a2bad441d_2368x932.png)](<https://substackcdn.com/image/fetch/$s_!DZpq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8d29b301-f48d-4272-ab5e-d36a2bad441d_2368x932.png>)

Comparing to the assembly above, the extra load-store are gone - first mystery solved.

_Issue source: compiler / programming language_

#### Issue 2: Data dependency hazard

The relevant part of the loop looked like this:

[![](https://substackcdn.com/image/fetch/$s_!XNLx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc16f2b15-20c0-4a02-a26f-c29deb8a4b0e_2080x932.png)](<https://substackcdn.com/image/fetch/$s_!XNLx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc16f2b15-20c0-4a02-a26f-c29deb8a4b0e_2080x932.png>)

Timing this loop as we varied stride showed that for the first few strides, increasing stride had _no effect on the time_ (solid lines in the plot below). With an Apple M2:

With the size of our loop, increasing stride definitely means more cache lines are touched, but it is making no difference. What’s going on?

Let’s look back at [the assembly](<https://godbolt.org/z/GqKzdPf7h>) (same as the previous snippet). 

If we manually unroll a few iterations, we have the following pattern:

[![](https://substackcdn.com/image/fetch/$s_!HVjb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3f4aaf66-bac6-4161-9cf9-b54ae4fd5e54_2080x752.png)](<https://substackcdn.com/image/fetch/$s_!HVjb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3f4aaf66-bac6-4161-9cf9-b54ae4fd5e54_2080x752.png>)

_FP add 2 cannot issue until FP add 1 has been committed_ , a classic Read-After-Write hazard. While a chip designer understands this very well, a programmer rarely needs to understand data dependency hazards in CPU pipelining. In this example, the float add dominates the effects from the load/store due to the data dependency and the long latency of floating-point add.

We add an unrolled version:

[![](https://substackcdn.com/image/fetch/$s_!XTJf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7842ccdc-f24c-464b-a074-42b9e2eb1bfc_2840x2464.png)](<https://substackcdn.com/image/fetch/$s_!XTJf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7842ccdc-f24c-464b-a074-42b9e2eb1bfc_2840x2464.png>)

The unrolled version time is significantly smaller, as visible in the dashed lines in the plot above, and more importantly, now we see the linear rise we had predicted.

_Issue source: microarchitecture, not visible in assembly instructions_

#### Issue 3: Warmup effects

After root-causing issue 2, to avoid dealing with the unrolled loop, we changed the accumulate to a Read-Modify-Write. The time for each iteration is now longer because a load and store are required for each iteration, which should make data movement costs the dominating factor.

[![](https://substackcdn.com/image/fetch/$s_!cAkz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fefff1b84-497c-4c57-93e9-41490759e252_2080x844.png)](<https://substackcdn.com/image/fetch/$s_!cAkz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fefff1b84-497c-4c57-93e9-41490759e252_2080x844.png>)

A number of stateful microarchitectural effects unrelated to the data cache contribute to performance characteristics, yet produce data cache-like behaviors. Such factors may include page table caching, page walk caching, prefetcher training, the memory controller, and even frequency ramping.

We attempted to stabilize the effect of these factors before running trials by running a warmup function at the beginning of the program. The warmup simply iterates over every element of data once to have the cache in a predictable state.

[![](https://substackcdn.com/image/fetch/$s_!Ef2a!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc01b55e4-f41d-40fc-95e0-0b83ebd0a1f0_2184x2732.png)](<https://substackcdn.com/image/fetch/$s_!Ef2a!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc01b55e4-f41d-40fc-95e0-0b83ebd0a1f0_2184x2732.png>)

The results:

The warmup appears to universally make the program faster, irrespective of the stride (more pronounced effect on a different system in plots below). Our best guess is that the warmup ramping up the CPU frequency is the dominant effect. We also considered a trial for one stride affecting another, but running a single stride per run of the program didn’t yield clearer results (and took much longer).

Again, if you have any better ideas, we would love to know - please leave a comment!

[Leave a comment](<https://www.avikde.me/p/cache-effects-in-object-oriented/comments>)

 _Issue source: microarchitecture / hardware_

#### Issue 4: Initial no-effect; second slope after cache line boundary

**4a)** In the previous plot, there is an initial part till about stride ~5 (20 bytes) where we predicted a linear rise, but instead see no effect of stride on timing.

While we are not sure, this is likely due to hardware prefetching: Modern CPUs have hardware prefetchers that detect sequential / strided access patterns and automatically fetch data ahead of time. Once the stride grows large enough (~20-64 bytes), the prefetcher can no longer keep up—either because it can’t fetch far enough ahead, or because the access pattern becomes too sparse for it to predict. At this point, we finally see the expected linear increase as each access genuinely waits for data from main memory.

**4b)** We expected the access time to plateau after each access was already hitting a different cache line. However, there appears to be a slower rise after the cache line boundary at least on the Apple M2 processor

Some (unconfirmed) hypotheses for the slower rise after the boundary:

  * L1 → L2 spilling if the working set exceeds L1 capacity, incorporating L2 access times

  * TLB misses as large strides access many different memory pages




 _Issue sources: microarchitecture / hardware_

#### Issue 5: Different behavior on different processors

Throughout uncovering the previous issues, we ran a few tests on other processors, and unfortunately that only served to increase the number of unknowns. In this section we will show you some of those results, but only be able to speculate about what causes them.

With an AMD Zen5 processor:

We see a plateau after an initial rise, which matches our naive prediction.

However, we observe a **peak around 32 floats (128 bytes) followed by a drop**. We don’t have an explanation for this behavior, which may be to do with advanced prefetcher behavior. In other words, the hardware may be making assumptions about our access pattern, and stride = 64-128 bytes hits the worst-case scenario where those assumptions fail. If you have any ideas about the cause, let us know in the comments!

[Leave a comment](<https://www.avikde.me/p/cache-effects-in-object-oriented/comments>)

We also tested on an Intel processor on Windows, which confirmed that some of the strangest aspects of the two plots above are to do with AMD, and not the compiler.

This resembles our Apple M2 plots more closely, including the slower rise after the cache line boundary. It also adds an even slower rise after 2x the cache line boundary.

_Issue sources: secret microarchitectural optimizations_

### Back to programming

Through this journey, it is safe to say we learned a lot about the complexity of modern processors. Fortunately, though, our central point about the (initial, then plateauing) rise of access time with stride still stands as universally true. Phew!

How do we utilize this knowledge as a programmer? **The key is to ensure that commonly-accessed data is packed tightly in contiguous memory.**

The naive OOP concept of owning data:

  * The class directly contains/owns the data as member variables

  * Example: Joint class with float sensed_position (and other things) embedded in it

  * This creates the AoS memory layout problem




**Instead store indices.** In the literature on data-oriented design, this is sometimes called: Entity-Component-System (ECS) pattern, or data-oriented design with handles.

  * The class contains references, pointers, or indices to data stored elsewhere

  * This allows you to keep polymorphism while avoiding AoS layout issues




**It isn’t object-oriented vs. polymorphism.** Just to reiterate that data-oriented is not opposed to OOP conveniences, consider that Pinocchio [uses polymorphism to specialize functions](<https://github.com/stack-of-tasks/pinocchio/blob/devel/include/pinocchio/multibody/joint/joint-model-base.hpp>), but stores indices to the vectors, not the data itself. The actual positions and velocities live in contiguous arrays, giving cache-friendly SoA layout, while the polymorphic joint models provide the OOP interface. You can have the benefits of polymorphism (different joint types with specialized behavior) without the memory layout problems of AoS. This is the middle ground between pure OOP with composition and abandoning OOP entirely for data-oriented design.

### Closing thoughts

In this post, we first showed how OOP-thinking can naturally lead to suboptimal cache usage, with several real examples. Then we looked at the effects this can have, uncovering many interesting “side-quest” root-causing exercises.

It isn’t coincidence that modern performance-critical systems say no to naive composed OOP:

  * **Machine learning** libraries will often select the data layout (NCHW etc.) [transparently](<https://mlsysbook.ai/book/contents/core/hw_acceleration/hw_acceleration.html#sec-ai-acceleration-memoryefficient-tensor-layouts-e250>), optimizing for cache locality.

  * **Pinocchio** , a robotics kinematics / dynamics library, has its functions [access array data](<https://github.com/search?q=repo%3Astack-of-tasks/pinocchio%20forwardKinematics&type=code>).

  * **Drake** , a larger robotics-oriented library, eventually [has data in arrays](<https://github.com/RobotLocomotion/drake/blob/master/multibody/tree/multibody_tree-inl.h>) below abstraction layers.

  * **[Unity DOTS](<https://unity.com/dots>)** stores all Transform data in packed arrays, not in GameObjects.

  * **Box2D v3.0** switched from OOP bodies to ID-based handles with SoA storage.

  * **[Unreal Mass Entity](<https://dev.epicgames.com/documentation/en-us/unreal-engine/mass-entity-in-unreal-engine>)** is an ECS system for high-object-count scenarios.




Even if in an isolated example the performance gain seems small, these patterns occur so frequently that they can [add up to large losses that are difficult to eliminate](<https://youtu.be/fHNmRkzxHWs>).

Thanks for reading! If you enjoyed this kind of full-stack analysis and root-causing, please share and subscribe for more posts on robotics, AI, and computing.

Thanks for reading min{power}! Subscribe for free to receive new posts and support my work.

[Share](<https://www.avikde.me/p/cache-effects-in-object-oriented?utm_source=substack&utm_medium=email&utm_content=share&action=share>)

### References and further reading

  * Code for demonstrations in this post, and more on [github](<https://github.com/avikde/caching-tester>)

  * “Better memory representation” in Jeff Dean’s “[Performance Hints](<https://abseil.io/fast/hints.html#better-memory-representation>)”

  * “[Efficiency with Algorithms, Performance with Data Structures](<https://youtu.be/fHNmRkzxHWs>)” - Chandler Carruth [CppCon 2014]. **Note:** I don’t fully agree with the statement (10:45) that “efficiency is only affected by algorithms” - a good example is the energetic cost of moving a byte from DRAM -> core being significantly higher than from L1, meaning the same algorithm with poor cache performance actually consumes more energy, in addition to completing slower.

  * [Data-Oriented Design and C++](<https://youtu.be/rX0ItVEVjHc>) \- Mike Acton [CppCon 2014] 

  * Explicit cache control via [software prefetching](<https://en.wikipedia.org/wiki/Cache_control_instruction>)
