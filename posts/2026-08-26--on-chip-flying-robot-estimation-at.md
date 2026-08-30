---
title: "On-Chip Flying Robot Estimation At 2 Milliwatts"
subtitle: "The Navion project shows that physics-informed design and numerical solvers can deliver enormous leaps in power-efficiency"
date: 2026-08-26
slug: on-chip-flying-robot-estimation-at
canonical_url: "https://www.avikde.me/p/on-chip-flying-robot-estimation-at"
topic: "Uncategorized"
concepts:
  []
source: Substack
author: Avik De
---

# On-Chip Flying Robot Estimation At 2 Milliwatts

![](https://substackcdn.com/image/fetch/$s_!DzAu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1490e0f-1b74-4fd7-bf25-d417a2c7cf2a_842x441.png)

*The Navion project shows that physics-informed design and numerical solvers can deliver enormous leaps in power-efficiency*

> Originally published: [2026-08-26](https://www.avikde.me/p/on-chip-flying-robot-estimation-at)

**Citations:** [[citations/nvidia-com|nvidia.com]] · [[citations/harvard-edu|harvard.edu]] · [[citations/mit-edu|mit.edu]] · [[citations/github-com|github.com]] · [[citations/arxiv-org|arxiv.org]] · [[citations/ieee-org|ieee.org]] · [[citations/viksnewsletter-com|viksnewsletter.com]] · [[citations/en-wikipedia-org|en.wikipedia.org]] · [[citations/chipinsights-net|chipinsights.net]]

---

The human brain consumes ~10 W, while [current humanoid robot brains](<https://blogs.nvidia.com/blog/jetson-thor-physical-ai-edge/>) consume power in the order of ~100 W (and trending upward, let alone datacenter brains).

This compute power is untenable for small robots. For example, the [first untethered flight of the RoboBee in 2018 consumed 120 mW](<https://seas.harvard.edu/news/2019/06/robobee-flies-solo>) (~1,000x smaller):

[![](https://substackcdn.com/image/fetch/$s_!uRYQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3bbdb1b5-0ca9-4e2e-9e80-2b7fe1da5ce3_800x800.png)](<https://substackcdn.com/image/fetch/$s_!uRYQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3bbdb1b5-0ca9-4e2e-9e80-2b7fe1da5ce3_800x800.png>)

So are we out of luck for intelligent, power-sipping robots?

Approximately 10 years ago, the [Navion IC](<https://navion.mit.edu/>) was developed from a collaboration between Vivienne Sze and Sertac Karaman’s labs at MIT.

[![](https://substackcdn.com/image/fetch/$s_!DzAu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1490e0f-1b74-4fd7-bf25-d417a2c7cf2a_842x441.png)](<https://substackcdn.com/image/fetch/$s_!DzAu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1490e0f-1b74-4fd7-bf25-d417a2c7cf2a_842x441.png>)The Navion chip next to a small flying robot.

The headlining feature was that it consumed **2 mW of power** to solve the state estimation problem for flying robots, making it fit well within the power envelope of micro-scale robots.

It’s hard to appreciate how little power that is. For reference, (per the Harvard article) a single bulb on a string of LED Christmas lights consumes ~50x Navions. A phone processor consumes ~5 W or 2,500x Navions. An NVIDIA Jetson Thor (lightly loaded) might consume ~50 W or 25,000x Navions. On top of that, this was with old 65nm CMOS technology, while the Thor is built on a TSMC 4N process.

In this article, we will take a look at what problem this chip solved, generalizable principles behind how they did it, and why we should care.

Thanks for reading! Subscribe for free to receive new posts and support my work.

## What Does Navion Do?

Navion’s task is to estimate the robot’s position from measurements made by a (stereo) camera and inertial measurement unit (IMU).

Position estimates can then be used for controlled flight through waypoints, avoiding collisions, etc. The figure below depicts the camera-observed landmarks _L i_, and the algorithm (hopefully) recovers the blue trajectory.

[![](https://substackcdn.com/image/fetch/$s_!Uzu7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F49a04521-e394-4023-9100-6b162256b29a_1132x477.png)](<https://substackcdn.com/image/fetch/$s_!Uzu7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F49a04521-e394-4023-9100-6b162256b29a_1132x477.png>)

This task is usually called visual-inertial odometry (VIO). Modifying the sensor suite yields a few variants: if the IMU is unavailable, the task is called visual odometry (VO), and if a stereo camera is not available, it is called monocular VO. Navion is designed to solve the stereo VIO problem (and can therefore generalize to the smaller tasks).

This is a common (and timeless!) problem in robotics — it’s easy to find papers spanning several decades with different solutions. I tried to find some alternate implementations with some results on the same dataset and energetic measurements to compare.

[DPVO](<https://github.com/princeton-vl/DPVO>) and [DPVO-QAT++](<https://arxiv.org/abs/2511.12653>) represent an accelerated neural-network based solution to the VO problem using monocular data. They solve a smaller problem (less data to manage), but report very good performance with accuracy comparable to, or surpassing, the Navion results.

In terms of throughput of algorithm output:

  * Xeon: 12 FPS

  * ARM Cortex-A15: 2 FPS

  * Navion chip: 19 FPS

  * RTX 4060: 15 FPS




(first 3 figures from the [2019 Navion JSSC paper](<https://ieeexplore.ieee.org/document/8600375>), last one from the DPVO-QAT++ paper).

Even though the accuracy and throughput are comparable, the power consumption (normalized as energy per output keyframe or Joules/KF) is wildly different:

  * Xeon: 3.6 Joules/KF

  * ARM Cortex-A15: 1.5 Joules/KF

  * Navion chip: 0.0023 Joules/KF

  * RTX 4060 TGP: ~3.5 Joules/KF1




That is on the order of ~1,000x power reduction for comparable accuracy and throughput!

Some papers [present methods for low-power VO](<https://ieeexplore.ieee.org/document/7927257>), but focus on a hovering application instead of a general VIO solution, making it difficult to make an apples-to-apples comparison.

If you’re aware of other comparable research I missed (or any other thoughts), let me know below!

[Leave a comment](<https://www.avikde.me/p/on-chip-flying-robot-estimation-at/comments>)

## How Did They Do It?

There is a comprehensive collection of presentations and papers at the [project website](<https://navion.mit.edu/>), but I wanted to take a big picture lens and go over three generalizable principles from the methodology used in this project.

### 1\. Architect around data movement, not operations

The AI “memory wall” has brought the [energetic cost of data transfer](<https://ieeexplore.ieee.org/document/6757323>) into public awareness.

Navion’s approach is to center the whole design around data movement. This method is gaining increasing traction in machine learning as it becomes an economically dominant workload. As an example, we can look at [SambaNova's design](<https://www.viksnewsletter.com/p/inside-sambanovas-inference-architecture>):

> Here is how SambaNova does it: They assign all the PCUs and PMUs on the chip to various parts of the inference process. As shown in the image below, you can literally gerrymander your way through memory and compute cores via the software compiler. The computations are done on the PCUs, and the intermediate weights and results are stored in the PMUs. In a sense, the SambaNova compiler predetermines the “dataflow” across the chip – that is, how to split up the available data units to perform different functions required for inference. By keeping the entire calculation process on the chip, the data never leaves the chip to external HBM memory.

[![](https://substackcdn.com/image/fetch/$s_!OQgn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F00115c6a-047b-49bc-bd03-98d69d0c0bd0_1384x897.png)](<https://substackcdn.com/image/fetch/$s_!OQgn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F00115c6a-047b-49bc-bd03-98d69d0c0bd0_1384x897.png>)The compiler creates a dataflow path through the physical chip (source: SambaNova)

Navion’s architecture does not predetermine dataflow through the chip via compilation, it is in fact hardcoded for the VIO application. The chip logic is all downstream of the main design decisions around the flow of data through the chip.

[![](https://substackcdn.com/image/fetch/$s_!YREy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd612089e-489b-44cd-9873-c4cfb010e56e_640x517.png)](<https://substackcdn.com/image/fetch/$s_!YREy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd612089e-489b-44cd-9873-c4cfb010e56e_640x517.png>)

First, they have completely eliminated the need for external memory storage (DRAM) for the VIO operation. Input from cameras goes directly to the bottom left of the chip, while IMU sensor data connects to the IMU front-end (IFE) in the top. The 854 kB of SRAM for its shared memory and register file are sized to fit exactly the needed data:

  * Repeated pixel transfers are avoided by sizing framebuffers to hold the data for all needed calculations.

  * Mathematical operations run in-place (writing outputs over inputs that are no longer needed).

  * Data is compressed to occupy less SRAM, explicitly trading off memory savings with performance.




The takeaways here are to start designing the chip not from the ALU, but from the I/O, memory storage, and dataflow.

[Subscribe now](<https://www.avikde.me/subscribe?>)

### 2\. Choose precision based on error accumulation patterns

A naive enumeration of the basic data structure sizes results in several megabytes, which increases power consumption and area cost:

[![](https://substackcdn.com/image/fetch/$s_!5G7Z!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4738ff08-ee02-4eab-b979-ae07993bf3b8_1841x728.png)](<https://substackcdn.com/image/fetch/$s_!5G7Z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4738ff08-ee02-4eab-b979-ae07993bf3b8_1841x728.png>)

Navion’s next trick is to use data and algorithm-aware compression, allowing memory requirements to hit the aforementioned 854 kB.

[![](https://substackcdn.com/image/fetch/$s_!R5AL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe8e8f3c4-8a65-4e6d-a183-e5bdf96b2450_984x606.png)](<https://substackcdn.com/image/fetch/$s_!R5AL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe8e8f3c4-8a65-4e6d-a183-e5bdf96b2450_984x606.png>)

We are now used to hearing about quantization in machine learning models, and as may be expected, it comes with a precision tradeoff. The interesting part of the Navion implementation is that they used characterization and algorithm-level error accumulation knowledge to decide on required precision.

On one extreme, image data is heavily compressed — they tried even down to 1 bit per pixel!

[![](https://substackcdn.com/image/fetch/$s_!N-yd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f2be692-0767-4e10-b376-6195d843e0c9_447x239.png)](<https://substackcdn.com/image/fetch/$s_!N-yd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f2be692-0767-4e10-b376-6195d843e0c9_447x239.png>)

A heavily quantized version is used for most parts of the algorithm.

In a stark contrast, double precision (64-bit) floats are used for the linear solver. Why would you waste so much storage for this component? I’ll let the paper explain itself:

> This is due to the fact that the VIO pipeline is an open-loop system. Therefore, as time goes on, the uncertainty of the state estimation keeps increasing and the condition number of the linear system increases; this causes the problem to be ill-defined and thus cannot be properly solved.

The takeaway: certain categories of computation are remarkably [robust to low-precision computations (e.g. deep neural networks)](<https://www.avikde.me/p/what-von-neumann-understood-about>), while a linear solver doesn’t have the same characteristics. To design an accurate low-power system, you need to identify which parts of the computation need what precision.

### 3\. MatMults aren’t everything

Neural network (NN) hardware acceleration is founded on matrix multiplication (MatMult) [acceleration using systolic arrays](<https://www.avikde.me/p/systolic-arrays-for-general-robotics>). TPUs, NPUs, GPUs have exploited this framework to optimize power-efficient solutions for NN inference in a simple, scalable hardware primitive.

However, matrix multiplication isn’t sufficient to solve all problems! The VIO problem (in Navion and many other implementations) can be reduced to a [nonlinear least-squares](<https://en.wikipedia.org/wiki/Non-linear_least_squares>) regression, which they solve using a single step of a [Gauss-Newton algorithm](<https://en.wikipedia.org/wiki/Gauss%E2%80%93Newton_algorithm>). In turn, this reduces to the solution of a linear equation _A*x = b_ , implemented in the “linear solver” part of the chip.

The main steps are a [Cholesky decomposition](<https://en.wikipedia.org/wiki/Cholesky_decomposition>) (since _A_ is positive-definite and symmetric) and [back-substitution](<https://en.wikipedia.org/wiki/Triangular_matrix#Forward_and_back_substitution>) (the Wikipedia links explain the required steps explicitly). In addition, the Navion chip explicitly leverages sparsity in the _A_ matrix.

How is that implemented in hardware?

The details are unfortunately not documented (as far as I have found), but we can make some guesses/conjectures about a possible implementation. The logic could be driven by FSMs that control one or more 64-bit floating-point ALUs. For intermediate operands, the paper refers to an 85-register double-precision register file and shared SRAM.

Standard Cholesky requires operations like:
    
    
    L[i,j] = (H[i,j] - sum(L[i,k]L[j,k])) / L[j,j]
    L[i,i] = sqrt(H[i,i] - sum(L[i,k]^2))

You can imagine how the FSM (potentially with microcode support!) would need to generate matrix row/column addresses, read operands, invoke arithmetic operations (add/subtract, multiply, reciprocal, square root), and write results back in place.

The takeaway here is to not limit imagination to matrix multiply, and recognize that linear or nonlinear optimization are possible to break down and map to hardware just as well!

[Subscribe now](<https://www.avikde.me/subscribe?>)

## Final thoughts

Navion is one of my favorite academic projects because of the breadth it covers from computer architecture to robotics algorithm development. Deep co-design and architectural resourcefulness paid off to deliver not just incremental improvement, but a _1,000x jump_ in power efficiency for similar accuracy and throughput.

Should we care?

Even if we aren’t involved in micro-robotics, the general principles are valuable. Other than reduced battery life, increased power consumption also introduces [cooling challenges](<https://www.avikde.me/p/how-thermals-constrain-robots-chips>). Some Navion-inspired power-efficient components could help make longer- and cooler-running robots at any size scale.

There is also a trade-off between application-specific and general-purpose development. While Navion is obviously a VIO-specific chip, VIO is a common function for robots of various size-scales. Whether you would accept that functional modularity or prefer a general-purpose brain ultimately comes back to the bitter lesson and [end-to-end robotics pipelines](<https://www.avikde.me/p/the-architecture-behind-end-to-end>) — a recurring theme on this blog!

_Thanks for reading! If you enjoyed this post, please like (❤️) and restack — it helps others find my writing. Subscribe to receive new posts._

[ Share](<https://www.avikde.me/p/on-chip-flying-robot-estimation-at?utm_source=substack&utm_medium=email&utm_content=share&action=share>)

[Subscribe now](<https://www.avikde.me/subscribe?>)

If you liked this article, we have been writing about co-design at . Check if out:

[![](https://substackcdn.com/image/fetch/$s_!Z-fT!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74222e4c-9d04-46aa-82ba-7d82759b48b9_512x512.png)Chip InsightsThe Search for the Perfect MicroarchitectureTinyXPU is back…Read more2 months ago · 27 likes · 1 comment · Bharath Suresh and Avik De](<https://chipinsights.net/p/the-search-for-the-perfect-microarchitecture?utm_source=substack&utm_campaign=post_embed&utm_medium=web&embedding_publication_id=7287367>)

1

Paper doesn’t report power consumption, but assuming desktop card was power limited for experiments, this is ~50% of TGP/FPS
