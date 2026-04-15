---
title: "Systolic arrays for general robotics, AI, and scientific computing"
subtitle: "MatMuls dominate today's accelerators, but the original vision was much broader"
date: 2026-03-12
slug: systolic-arrays-for-general-robotics
canonical_url: "https://www.avikde.me/p/systolic-arrays-for-general-robotics"
topic: "Systolic Arrays"
concepts:
  - "Matrix Multiplication"
  - "Hardware Acceleration"
  - "Signal Processing"
  - "Neural Network Accelerators"
source: Substack
author: Avik De
---

# Systolic arrays for general robotics, AI, and scientific computing

![](https://substackcdn.com/image/fetch/$s_!YIQz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F932fc917-c77d-4254-b4b4-29c99149e1b5_1138x596.png)

*MatMuls dominate today's accelerators, but the original vision was much broader*

> Originally published: [2026-03-12](https://www.avikde.me/p/systolic-arrays-for-general-robotics)

**Topic:** [[topics/systolic-arrays|Systolic Arrays]]
**Concepts:** [[concepts/matrix-multiplication|Matrix Multiplication]] · [[concepts/hardware-acceleration|Hardware Acceleration]] · [[concepts/signal-processing|Signal Processing]] · [[concepts/neural-network-accelerators|Neural Network Accelerators]]
**Citations:** [[citations/seas-harvard-edu|seas.harvard.edu]] · [[citations/en-wikipedia-org|en.wikipedia.org]] · [[citations/spectrum-ieee-org|spectrum.ieee.org]] · [[citations/modernrobotics-northwestern-edu|modernrobotics.northwestern.edu]] · [[citations/github-com|github.com]] · [[citations/kwokanthony-medium-com|kwokanthony.medium.com]] · [[citations/eecs-harvard-edu|eecs.harvard.edu]] · [[citations/swh-princeton-edu|swh.princeton.edu]] · [[citations/arxiv-org|arxiv.org]] · [[citations/chipinsights-net|chipinsights.net]]

---

The TPU (Tensor Processing Unit), introduced by Google in a whirlwind project ~2015, has now become synonymous with hardware acceleration for deep neural networks. I’ve listed some references below on further reading on the TPU (I’d especially recommend ’s [historically-situated introduction](<https://thechipletter.substack.com/p/googles-first-tpu-architecture>)), but at the core of the TPU is a matrix multiplication unit (MXU) that achieves high-throughput and highly-efficient matrix multiplication. Since then, the concept has been integrated into a huge variety of hardware accelerators for neural networks (Groq LPU, NVIDIA Tensor Cores, Apple Neural Engine, Qualcomm Hexagon, and most NPUs), so you may think that it was Google’s ML inference ambitions that started this [cambrian explosion](<https://thechipletter.substack.com/p/ai-accelerators-the-cambrian-explosion>) in matrix multiplication acceleration — but that would be almost 40 years off the mark.

All these matrix multiplication units are based on the systolic array, an architectural concept invented by HT Kung at Carnegie Mellon University in the late _1970’s_. And Kung’s group didn’t stop at matrix multiplication, they presented a concept of systolic _networks_ of arbitrary processing _nodes_ that could do way more. While some of those concepts appear in niche signal-processing ASICs today, the dominance of deep neural networks over the last decade has caused this history and potential to be significantly overlooked in my opinion.

[![](https://substackcdn.com/image/fetch/$s_!Bf6n!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ca0876d-d71e-47d0-8e37-2550cd332955_267x267.jpeg)](<https://substackcdn.com/image/fetch/$s_!Bf6n!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ca0876d-d71e-47d0-8e37-2550cd332955_267x267.jpeg>)[HT Kung](<https://seas.harvard.edu/person/ht-kung>)

My interest in this (and the goal of this article) is twofold: (1) Shine a spotlight on this fascinating research and preview the types of problems that can be solved with systolic architectures. (2) Dig into and potentially uncover jumps in performance and efficiency for AI and robotics. I believe that holistic full-stack understanding and optimization (bringing together algorithms and hardware) will be key in advancing these technologies.

Beyond this post, we won’t stop at a theoretical overview — leveraging the computer engineering experience and story-telling of  we will actually build up accelerators to use in general-purpose robotics, AI, and scientific applications. We have an article coming soon with the first step, so make sure to subscribe!

[Subscribe now](<https://www.avikde.me/subscribe?>)

### Why systolic architectures

A systolic architecture is characterized by a network of processing elements (PE) that feed data to each other instead of going to the memory hierarchy for operands.

[![](https://substackcdn.com/image/fetch/$s_!YIQz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F932fc917-c77d-4254-b4b4-29c99149e1b5_1138x596.png)](<https://substackcdn.com/image/fetch/$s_!YIQz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F932fc917-c77d-4254-b4b4-29c99149e1b5_1138x596.png>)Systolic array concept from Kung (1982)

The core benefits are:

  * It alleviates **memory bottlenecks** by allowing multiple compute operations to occur without going to memory (as nicely depicted by the figure above). The design can allow computation time to be balanced with I/O if designed properly, avoiding one stalling due to the other.

  * It can create **simple, regular designs** → a modular setup that can be extended for different functions. It is relatively easy to write the RTL!

  * 2D arrays can very easily be **deeply pipelined** (as we will see below), naturally taking advantage of algorithm concurrency.




The PE network can look like a 1D array (pictured above), 2D array (the most common today), or even other connections for specialized computations. 

[![](https://substackcdn.com/image/fetch/$s_!2-0_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04a2f9db-3619-43fa-a752-6a6278ab3ab9_716x186.png)](<https://substackcdn.com/image/fetch/$s_!2-0_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04a2f9db-3619-43fa-a752-6a6278ab3ab9_716x186.png>)Another figure from Kung (1982) — connections depend on the number of inputs and outputs for each PE.

Data flows between cells in a pipelined fashion, and communication with the outside world is at boundary cells.

### The foundation of TPU — a MAC systolic network

[![](https://substackcdn.com/image/fetch/$s_!R98b!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feea556ec-2fc8-45c1-bcce-b7ebf6a543b2_200x240.png)](<https://substackcdn.com/image/fetch/$s_!R98b!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feea556ec-2fc8-45c1-bcce-b7ebf6a543b2_200x240.png>)

A **multiply-accumulate (MAC)** PE has two input edges and two output edges. In the form drawn below (“weight-stationary”), the weight _w_ is a parameter loaded into the PE. The data _x_ flows in and is passed unchanged left to right, and the current “accumulation” _b_ flows in from the top (usually from a PE connected to the north). The PE does the multiply-accumulate (_x * w + b_) and passes the accumulated sum down. We assume that the calculation happens in a single “tick” or clock cycle.

A PE in a systolic network is typically a simple compute primitive. Its power comes from connections to other PEs to express complex calculations.

The easiest way to understand how a weight-stationary systolic _array_ works is to understand how a **dot product** is computed. This is shown in the following image for 3 cycles, and we will walk through the computation.

[![](https://substackcdn.com/image/fetch/$s_!MCl3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd85f3020-8db6-4b67-8b17-ccc2f728ac47_716x638.webp)](<https://substackcdn.com/image/fetch/$s_!MCl3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd85f3020-8db6-4b67-8b17-ccc2f728ac47_716x638.webp>)Read this image column-wise, starting from the left.

In each cycle, a new entry of _x_ appears from the left, and one term is added to the dot product. The column of PEs contains a vector of weights. In each cycle, one term of the dot product is accumulated, and after 3 cycles, we have accumulated the full dot product _**b + w·x**._

We now draw the exact same operation, but in an abridged form (not showing the intermediate calculations and instead just showing the inputs and outputs at the ticks they appear).

  * A column of the array is drawn as _vector_ weight _w i_

  * The inputs are drawn as a diagonal (and enters the array skewed in time)

  * The output is shown at the bottom, appearing after _R_ cycles from when the input hits row 1, where _R_ is the number of PE’s in the column




[![](https://substackcdn.com/image/fetch/$s_!UyAL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe93d60b2-dbc1-4100-92e6-1d8001182424_942x494.webp)](<https://substackcdn.com/image/fetch/$s_!UyAL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe93d60b2-dbc1-4100-92e6-1d8001182424_942x494.webp>)

In this form it is easy to see that we are **pipelining** different _x i_ by starting the second one the cycle after the first one. The initial accumulator value can be set to _b i_, an affine bias.

So, with a single column systolic array, holding a column vector _w_ , we are computing _**y = b + X·w**_ , where the rows of _X_ are _x 1_, _x 2_, …

It is also noting the latency between when the _x i_ starts getting input to when we receive the output: The first element of _x 1_ enters the array at time _t=1_ , and we get the result out at _t=R_ , so the latency is _R-1_ cycles.

Making this a **2D array** (recall that the input x’s are bypassed to the right from each PE), we see that _x i_ will just arrive to interact with _w 2_ one cycle later. We can appropriately skew the columns of the B matrix:

[![](https://substackcdn.com/image/fetch/$s_!X1yw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F635ea2c7-b84a-4cd5-af8a-ce5e97983ad5_960x760.webp)](<https://substackcdn.com/image/fetch/$s_!X1yw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F635ea2c7-b84a-4cd5-af8a-ce5e97983ad5_960x760.webp>)

The operation that is executes is _**Y = B + X·W**_ , where _b ij _above is in row _i_ and column _j_ of _B_ , _W = [w1, w2]_ is the fixed weight matrix loaded in first. If _W_ is _n×n_ , and _X_ is _m×n_ , the matrix product is _O(mn 2)_ operations (as is standard), but due to the **structurally-enforced pipelining** , it was completed in _O(m+n)_ cycles!

And just like that, with a very simple MAC-computing PE, we can build up the matrix multiplication hardware unit that is the core of most AI hardware accelerators.

There is much more to be said about how it is implemented in RTL, how it performs, how the matrix shapes affect utilization, the total latency, throughput and efficiency benefits. We will go over that and intuitive insights in an upcoming  post. In the remainder of this article, we will turn our attention to other, more overlooked, uses of systolic networks in applications to broader AI, robotics, and numerical methods.

Thanks for reading min{power}! Subscribe for free to receive new posts and support my work.

### Moving beyond MAC

Keeping the exact same 2D array structure and the skewed input feeding, observe that we had two underlying binary operations: the PE (node) computed **multiply (**_**·**_**)** and the arrow (edge) computed **sum (+)**. In general, the array will compute the result with those operators replaced by any counterparts: **(**_**x 1**_**⊙** _**w 1**_**) ⊕ (**_**x 2**_**⊙** _**w 2**_**) ⊕ ⋯**

I’ll be brief with these and list further reading below, and try to draw special attention to ones that are interesting for applications in robotics and AI.

#### 1) Pattern matching (Kung group)

Using logical and (∧) and logical or (∨) as the operations: _**y**_**= (**_**x 1**_**∧** _**w 1**_**) ∨ (**_**x 2**_**∧** _**w 2**_**) ∨ ⋯**

This will return **1** if the vector _x_ matches the vector _w_ , and **0** otherwise.

#### 2) Sorting (Kung group)

This one is fascinating and intuitive. Each PE performs a simple compare and swap operation, and passes the max downward and the min rightward. With _n_ rows and _n_ columns, it will execute the [odd-even sort](<https://en.wikipedia.org/wiki/Odd%E2%80%93even_sort>) algorithm and produce the sorted array.

A glance at that wikipedia page reveals both a weakness and a strength of systolic arrays. They can only execute algorithms that can work based on local connections (the odd-even sort takes _O(n 2)_ operations, vs. more optimal algorithms), but as in matrix multiplication above, the latency is _O(n)_. While the best sort algorithm takes _O(n log n)_ steps sequentially in scalar hardware, the systolic network lets suboptimal algorithms complete with lower latency.

#### 3) 2D motion planning

Deterministic motion planning (identifying environmental obstacles and planning a path through free areas respecting the system dynamics) is a fundamental problem in robotics. About 10 years ago there was even attempt to [build chips to solve this problem](<https://spectrum.ieee.org/motionplanning-chip-speeds-robots>).

[![](https://substackcdn.com/image/fetch/$s_!kdee!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa234c2f2-602f-4c18-b417-0d6a2b1390f9_684x628.png)](<https://substackcdn.com/image/fetch/$s_!kdee!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa234c2f2-602f-4c18-b417-0d6a2b1390f9_684x628.png>)Grid-based motion planning using dynamic programming ([source](<https://modernrobotics.northwestern.edu/nu-gm-book-resource/10-4-grid-methods-for-motion-planning/>))

Dynamic programming solutions (including Dijkstra’s algorithm, A*) can be implemented by local and iterative propagation from the goal, and just as with odd-even sort, the nearest-neighbor connection pattern can be mapped well to a systolic array.

Unfortunately, the number of grid cells grows exponentially with the dimension of the ambient space, and this is problematic if we need to have one PE per cell. This makes systolic motion planning impractical unless we only have a 2D problem to solve, but I think it is an interesting application nonetheless.

#### 4) Stereo vision semi-global matching

A PE that accumulates matching costs along a scanline can be used to form a systolic array that implements [semi-global matching](<https://en.wikipedia.org/wiki/Semi-global_matching>) (SGM). This algorithm is used to calculate disparity in the very popular [Intel RealSense camera ASICs](<https://github.com/realsenseai/librealsense/discussions/11586>).

[![](https://substackcdn.com/image/fetch/$s_!YcYE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46126588-8883-46e7-8186-8ba28ce42e09_250x250.png)](<https://substackcdn.com/image/fetch/$s_!YcYE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46126588-8883-46e7-8186-8ba28ce42e09_250x250.png>)Grid-based SGM depiction ([source](<https://en.wikipedia.org/wiki/Semi-global_matching>))

SGM systolic arrays on FPGAs run this at pixel rate, processing one scanline per clock, and deterministic low-latency computation is obviously paramount here.

#### 5) Matrix decompositions for numerical methods

To some extent, I’ve saved the most promising (at least in my view) for last. Matrix decompositions that aid in factorization are key to solving systems of equations, and this is ubiquitous in all sorts of robotics and general problems.

**5.1) QR decomposition.** This matrix factorization is the numerically stable way to solve **least squares or pseudoinverses** in overdetermined systems, and has applications to robot kinematics, SLAM, sensor fusion, online parameter estimation, etc. Additionally, it is a key component of **quadratic program (QP) solvers** : in active set solvers after the active set is identified, for Jacobian factorization in SQP, etc. These workloads are important in [low-level control in robotics](<https://www.avikde.me/p/the-architecture-behind-end-to-end>) and typically need deterministic and low-latency solutions. The Givens rotations method (gentle explainer [here](<https://kwokanthony.medium.com/detailed-explanation-with-example-on-qr-decomposition-by-givens-rotation-6e7bf664fbdd>)) performs local operations on 2x2 submatrices, which lends itself very well to locally-connected CORDIC-implementing PEs in a systolic array.

**5.2) Cholesky decomposition for symmetric positive-definite (SPD) matrices.** This is a slightly easier factorization if the matrix is SPD, which comes up for example in state estimation, Kalman filtering, normal equations in interior point methods, etc. These workloads would come up in dedicated state estimation blocks in robotics pipelines. For decomposing _A = LL T_ with lower-triangular _L_ , each PE computes one entry of L using only its left and upper neighbors, making the data dependencies purely local. This is repeated on the smaller matrix till completion.

Both of the systolic implementations referred to above use non-MAC PEs, and a triangular (not rectangular) network — this is very uncommon in current hardware, but was represented in the Kung references above.

For this post, I wanted to stick to high-level intuitive descriptions, but in the open-source [TinyXPU project](<https://github.com/avikde/tiny-xpu>), we will aim to implement and analyze some of these non-traditional systolic networks for robotics and AI pipelines. Stay tuned for the upcoming post introducing this project!

[Subscribe now](<https://www.avikde.me/subscribe?>)

### Conclusion

Systolic arrays were both invented before people think, and are more general than people think. They can have deterministic (no cache misses) **high throughput and energy efficiency** for algorithms which can work on local data. However, they are bad for working with sparse data (e.g. for sparse linear system solving), and bad for algorithms that need global data (e.g. Householder QR, which needs to operate on a full matrix column at a time).

In the deep neural network boom, the MAC array is so dominant in workload (>95% of operations in any DNN) that the non-MAC compute takes a tiny fraction of time. Dedicating a full systolic array with _n 2_ PEs to non-MAC operations would be area-inefficient for neural net workloads. This is why commercial vendors have not explored the co-design of systolic networks with algorithms, including PEs that can do MAC but also other functions like Givens rotations on one chip. For robotics workloads and other general scientific methods, the mix of primitives is different and (in my opinion) worth revisiting.

### Further reading

  * [Kung 1982: Why Systolic Architectures](<https://www.eecs.harvard.edu/~htk/publication/1982-kung-why-systolic-architecture.pdf>) \- Great high-level overview of the motivation beyond systolic architectures

  * [Kung 1982: VLSA Array Processors](<https://swh.princeton.edu/~kung/papers_pdf/New%20Folder/VLSI%20Array%20Processors.pdf>) \- Further detail on applications such as QR decomposition

  * [Google TPU v1 paper](<https://arxiv.org/pdf/1704.04760>)




Related posts:

[![](https://substackcdn.com/image/fetch/$s_!Z-fT!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74222e4c-9d04-46aa-82ba-7d82759b48b9_512x512.png)Chip InsightsMapping algorithms to custom silicon - Part 1Read more2 months ago · 22 likes · Bharath Suresh and Avik De](<https://chipinsights.net/p/mapping-algorithms-to-custom-silicon?utm_source=substack&utm_campaign=post_embed&utm_medium=web>)
