---
title: "Power-efficient and safe mobile robots"
subtitle: "Talk at OSU CoRIS seminar"
date: 2024-12-23
slug: power-efficient-safe-robots
canonical_url: "https://www.avikde.me/p/power-efficient-safe-robots"
tags:
  - robotics
  - research
concepts:
  - "Insight"
  - "Book"
  - "Modules"
  - "Modularity"
  - "Digital"
source: Substack
author: Avik De
---

# Power-efficient and safe mobile robots

![](https://substackcdn.com/image/fetch/$s_!bxUH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b242a66-55dd-4508-ac58-f91691035686_600x600.jpeg)

*Talk at OSU CoRIS seminar*

> Originally published: [2024-12-23](https://www.avikde.me/p/power-efficient-safe-robots)

**Topics:** [[topics/robotics|Robotics]] · [[topics/research|Research]]
**Concepts:** [[concepts/insight|Insight]] · [[concepts/book|Book]] · [[concepts/modules|Modules]] · [[concepts/modularity|Modularity]] · [[concepts/digital|Digital]]
**Citations:** [[citations/engineering-oregonstate-edu|engineering.oregonstate.edu]] · [[citations/en-wikipedia-org|en.wikipedia.org]] · [[citations/mitpress-mit-edu|mitpress.mit.edu]] · [[citations/directory-seas-upenn-edu|directory.seas.upenn.edu]] · [[citations/deepblue-lib-umich-edu|deepblue.lib.umich.edu]] · [[citations/pmc-ncbi-nlm-nih-gov|pmc.ncbi.nlm.nih.gov]] · [[citations/sciencedirect-com|sciencedirect.com]] · [[citations/science-org|science.org]] · [[citations/waymo-com|waymo.com]] · [[citations/ieeexplore-ieee-org|ieeexplore.ieee.org]] · [[citations/worldscientific-com|worldscientific.com]] · [[citations/nature-com|nature.com]] · [[citations/technologyreview-com|technologyreview.com]] · [[citations/dl-acm-org|dl.acm.org]] · [[citations/thenextweb-com|thenextweb.com]] · [[citations/direct-mit-edu|direct.mit.edu]] · [[citations/compositionalintelligence-github-io|compositionalintelligence.github.io]]

---

I gave a [talk at OSU’s CoRIS seminar](<https://engineering.oregonstate.edu/events/power-efficient-autonomous-mobile-robots>). It was a joy to visit OSU’s Robotics department. The faculty are driven to solve problems grounded in the real world, in application areas ranging from under the sea to the peak of Mt. Hood. Also, it was only partially raining on the day of the seminar (which I found out was a rarity).

[![OSU](https://substackcdn.com/image/fetch/$s_!bxUH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b242a66-55dd-4508-ac58-f91691035686_600x600.jpeg)](<https://substackcdn.com/image/fetch/$s_!bxUH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b242a66-55dd-4508-ac58-f91691035686_600x600.jpeg>)The [PNW](<https://en.wikipedia.org/wiki/Pacific_Northwest>) scenery is terrific and would be a great draw if it didn’t mostly rain from September to May.

## Modularity

In this talk, I started a bottom-up exploration of composition in robotics.

Thanks for reading min{power} by avikde! Subscribe for free to receive new posts.

### Dynamic legged locomotion

As with I’m sure many others, as a young graduate student, I was inspired by the dynamic legged locomotion work at the MIT Leg Lab in the 1980’s:

In his thought-provoking [book](<https://mitpress.mit.edu/9780262681193/legged-robots-that-balance/>), [Raibert](<https://en.wikipedia.org/wiki/Marc_Raibert>) articulated an intriguing idea called “Control of Running Decomposed into Three Parts.” Researchers have been trying to understand when and how this may be possible, and how it generalizes, since then.

My Ph.D. advisor, [Koditschek](<https://directory.seas.upenn.edu/daniel-e-koditschek/>), has been doing that for decades. In the 1990’s, his research group built and impressive array of juggling robots (as a less-power-hungry proxy for cyclic dynamical behavior):

In the course of the juggling research, they introduced a formal idea of [sequential composition](<https://deepblue.lib.umich.edu/bitstream/handle/2027.42/67990/10.1177_02783649922066385.pdf>) with an intuitive but mathematically rigorous and useful idea:

[![Sequential Composition in IJRR '99](https://substackcdn.com/image/fetch/$s_!Z6_V!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F780dd6e7-06fb-48b3-aeee-c5ae20d7f8d4_400x407.png)](<https://substackcdn.com/image/fetch/$s_!Z6_V!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F780dd6e7-06fb-48b3-aeee-c5ae20d7f8d4_400x407.png>)The “funnels” picture of sequential composition

Analogously, we can retroactively label Raibert’s “control in three parts” idea as an example of [parallel composition](</jerboa-hopping-video>). While the term is not extremely common in the robotics literature, similar concepts appear with names such as “decoupled control”. The idea has clearly been empirically useful, but [formalizing it](</hybrid-averaging>) has been quite tricky with any degree of generality.

Sequential and parallel composition are a very intuitive idea with equivalents in programming and spoken language. Consider the example of generating spoken language – instead of outputting the sounds corresponding to an entire sentence at once, we may want to start by assembling words from [phonemes](<https://en.wikipedia.org/wiki/Phoneme>), and assembling those into sentences. On the other hand, modern [deep learning speech synthesis](<https://en.wikipedia.org/wiki/Deep_learning_speech_synthesis>) may not have any such compositional properties, which is an intentional counterpoint that we will return to.

### Modularity elsewhere

Deep learning did evolve from neural networks, which evoke biology right in the name. Biology has [inspired many of the working principles](</what-are-robot-dogs>) of quadrupedal robots, including behavioral modularity.

Animals have an abundance of sensory inputs and muscle, but the number of task-level variables important to any particular task is a lot smaller ([Ting (2007)](<https://pmc.ncbi.nlm.nih.gov/articles/PMC4121431/>)). Going further, [Ting et. al. (2015)](<https://www.sciencedirect.com/science/article/pii/S0896627315001579>) argues that motor modules arise from neural plasticity in spinal structures that selective coordinate and co-activate multiple muscles. The result is that animals can control tasks like balancing in a hierarchical fashion, keeping the dimension of the task-space control low.

[![Modules in Biology](https://substackcdn.com/image/fetch/$s_!8aEl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5335aabb-38d5-4b28-a7d5-b4b07775e040_1712x750.png)](<https://substackcdn.com/image/fetch/$s_!8aEl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5335aabb-38d5-4b28-a7d5-b4b07775e040_1712x750.png>)Modularity in biology

While robots typically have fewer actuators than an animal has muscles, each individual task will typically be overactuated for a general-purpose robot. For example, a humanoid robot will not need its arms to maintain a standing posture.

If we accept the presence of these motor modules, these patterns of activation could be re-used for different behaviors. Quoting [Ting et. al. (2015)](<https://www.sciencedirect.com/science/article/pii/S0896627315001579>):

> Multifunctionality: muscles can contribute to many actions; a few muscles can be combined in many ways to produce a wide range of different actions.

Making equivalences to the synthetic disciplines, there is a clear connection to the idea of re-using behavioral modules, as we showed with [Minitaur vertical hopper compositions](</vertical-hopper-compositions>).

Putting it all together, I’d argue that there are equivalences between biology and robotics in three distinct aspects of modularity:

[![Modularity is Everywhere](https://substackcdn.com/image/fetch/$s_!WRpR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe86aebea-3af7-475f-9828-6ceb76c5f8a9_1341x290.png)](<https://substackcdn.com/image/fetch/$s_!WRpR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe86aebea-3af7-475f-9828-6ceb76c5f8a9_1341x290.png>)

### Modularity benefits

Some of the benefits of modularity that are enjoyed by biological systems can also apply to the synthetic disciplines as well.

Motor modules can help navigate a “difficult-to-search and nonlinear set of neuromechanical solutions for movement” ([Ting et. al. (2015)](<https://www.sciencedirect.com/science/article/pii/S0896627315001579>)) as well as the “curse of dimensionality” in various engineering disciplines. This has clear implications on the computational requirements for algorithms.

A slightly less obvious use case for modularity is for optimizing robot design for [flapping](</template-based-design-robobee>), [jumping](<https://www.science.org/doi/abs/10.1126/scirobotics.aag2048>), etc., using coordinated movement patterns (or, template trajectories).

## Real-world robotics

As robotics tools proliferate, their side-effects will start to also have a larger and larger impact on society.

### Safety and predictability

The autonomous vehicle industry is possibly the first (but certainly not the last) subfield that has been thrust into the limelight of the question of safety of autonomous systems. The responsible peer-reviewed efforts of the first-party companies (e.g. [Waymo](<https://waymo.com/safety/research/>)) are huge steps in the right direction, but that is certainly not the end of the story.

Robustness and multiple solutions inherent to a modular structure (as we saw above) is in stark contrast to the weakness of monolithic AI structures when subject to uncertainty ([Cummings](<https://ieeexplore.ieee.org/document/10778107>)).

Intuitively, a modular architecture can be “debugged” and intermediate outputs can be logged and inspected. Just like a black box recording of an aircraft allows review of inputs made from the pilot to the machine, a modular structure allows insight into, and thresholding of, the function of individual modules:

[![Safety and Predictability](https://substackcdn.com/image/fetch/$s_!LINj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e5500cc-b94c-42c8-b339-edb5d6050dab_800x278.png)](<https://substackcdn.com/image/fetch/$s_!LINj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e5500cc-b94c-42c8-b339-edb5d6050dab_800x278.png>)Safety via modularity

### Energy

While mechanical work done by robots necessarily needs energetic input (and the conversion efficiency can be [quite high](<https://www.worldscientific.com/doi/abs/10.1142/9789814415958_0057>)), the cost of computational work is nowhere close to the only known fundamental energetic limit based on [Landauer’s principle](<https://en.wikipedia.org/wiki/Landauer%27s_principle>).

Even as chips get more and more efficient, our appetite for computation outstrips those benefits, raising [continual](<https://www.nature.com/articles/d41586-024-03408-z>) [concern](<https://www.technologyreview.com/2024/12/13/1108719/ais-emissions-are-about-to-skyrocket-even-further/>).

[![Energy](https://substackcdn.com/image/fetch/$s_!uomH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b3a3b5a-49a0-49f2-a29c-212fdc1884a6_1110x502.png)](<https://substackcdn.com/image/fetch/$s_!uomH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b3a3b5a-49a0-49f2-a29c-212fdc1884a6_1110x502.png>)“AI’s energy crisis”

As already recognized by biology, a growing community of researchers are exploiting the fact that [modular neural networks reduce power consumption](<https://dl.acm.org/doi/10.1145/3408062>).

## The case for compositionality

Modularity comes with a price. The motor modules in humans have appeared over the (long) course of animal evolution, and the modular control structures developed for robots need to be hand-crafted. These processes are much less automatic, and [need more work than](<https://en.wikipedia.org/wiki/Attention_Is_All_You_Need>) scaling a simple structure with more data. In fact, the importance of pushing for architectural progress may not be limited to robotics ([LeCun](<https://thenextweb.com/news/meta-yann-lecun-ai-behind-human-intelligence>)).

Additionally, modularity necessarily imposes limits on the space of usable methods or algorithms. For example, a modular controller reasoning with the equivalent of “motor modules” for a triple pendulum would never be able to accomplish this:

Nevertheless, the question of system abstraction with modularity has come up before in other fields such as digital VLSI and programming languages, and has clearly won out, in part due to the reasons discussed above.

[![Abstraction](https://substackcdn.com/image/fetch/$s_!TNPx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F953e7f36-aba1-48f3-a58c-4bd53d608b23_800x388.png)](<https://substackcdn.com/image/fetch/$s_!TNPx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F953e7f36-aba1-48f3-a58c-4bd53d608b23_800x388.png>)Abstraction in computer engineering

We don’t yet have a generally accepted methodology or architecture in robotics that could be a foundation for symbolic behavior programming.

End-to-end deep neural networks have become a useful and generally-accepted architecture without compositional properties, but neural networks are not necessarily incompatible with compositionality ([Hinton](<https://direct.mit.edu/neco/article/35/3/413/114140/How-to-Represent-Part-Whole-Hierarchies-in-a>), [Marcus](<https://compositionalintelligence.github.io/pdfs/Marcus.pdf>)). For more on this topic, I highly recommend the proceedings of this workshop on [The Challenge of Compositionality for AI](<https://compositionalintelligence.github.io/>).

What is the path forward?

If we value the benefits of modularity discussed above, it will take more work to develop the correct architectures, but this work is essential to get to the point of robotics becoming a true scientific discipline with predictable outcomes.
