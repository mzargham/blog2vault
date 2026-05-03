---
title: "The First Paradigm in Robotics & AI Research: Lessons from Computer Engineering"
subtitle: "Commoditization and end-to-end learning have consolidated robotics and AI. What's next for research labs?"
date: 2026-04-29
slug: the-first-paradigm-in-robotics-and
canonical_url: "https://www.avikde.me/p/the-first-paradigm-in-robotics-and"
topic: "Paradigm Shifts In Robotics And Ai Research"
concepts:
  - "Commoditization"
  - "End-to-End Robotics Pipelines"
  - "World Models"
source: Substack
author: Avik De
---

# The First Paradigm in Robotics & AI Research: Lessons from Computer Engineering

![](https://substackcdn.com/image/fetch/$s_!4P2l!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c9a075c-f936-4270-8785-4812da0b85e4_956x680.png)

*Commoditization and end-to-end learning have consolidated robotics and AI. What's next for research labs?*

> Originally published: [2026-04-29](https://www.avikde.me/p/the-first-paradigm-in-robotics-and)

**Topic:** [[topics/paradigm-shifts-in-robotics-and-ai-research|Paradigm Shifts In Robotics And Ai Research]]
**Concepts:** [[concepts/commoditization|Commoditization]] · [[concepts/end-to-end-robotics-pipelines|End-to-End Robotics Pipelines]] · [[concepts/world-models|World Models]]
**Citations:** [[citations/en-wikipedia-org|en.wikipedia.org]] · [[citations/ghostrobotics-io|ghostrobotics.io]] · [[citations/businessinsider-com|businessinsider.com]] · [[citations/youtube-com|youtube.com]] · [[citations/kr-asia-com|kr.asia.com]] · [[citations/rpg-ifi-uzh-ch|rpg.ifi.uzh.ch]] · [[citations/rsl-ethz-ch|rsl.ethz.ch]] · [[citations/bostondynamics-com|bostondynamics.com]] · [[citations/arxiv-org|arxiv.org]] · [[citations/yourownrobot-ai|yourownrobot.ai]] · [[citations/github-com|github.com]] · [[citations/pi-website|pi.website]] · [[citations/berkeley-edu|berkeley.edu]] · [[citations/acm-org|acm.org]] · [[citations/thwink-org|thwink.org]] · [[citations/sciencedirect-com|sciencedirect.com]]

---

[Thomas Kuhn wrote](<https://en.wikipedia.org/wiki/The_Structure_of_Scientific_Revolutions>) that scientific fields develop into dominant _paradigms_ that characterize phases of productive but incremental research. The very existence of a paradigm is evidence to the maturation of a field.

For robotics, we may be in the midst of the first time this has ever happened.1 The start of our research careers resembled the “wild west” of emerging techniques and technologies, but ideas have converged more now. On one hand, robotic hardware has gotten good enough to see thousands of robots of getting shipped and used, by consumers and researchers alike. On the algorithm side, the bitter lesson and its corollary — hypothesized “scaling laws” — have provided a scaffolding around which progress can be evaluated. [End-to-end behavior cloning policies](<https://itcanthink.substack.com/p/vision-language-action-models-and>) seem like they can generalize to all sorts of tasks, and performance predictably improves with more data. We’ll refer to these two trends as _commoditization_ and _architectural convergence_ , and discuss how they shape the current paradigm below.

The establishment of this current paradigm has also had side-effects on the nature of research that may in themselves be setting us up for paradigm _shifts_. While it is a bit of an overreach to use the term “revolution” for robotics (as Kuhn did for science), such a shift would be pivotal for researchers and is worth understanding.

_This article is co-written by_ _and_ _, both robotics researchers with experience in academia as well as industry. Chris writes about AI and robotics, and Avik writes about robotics, computing, and AI._

[![](https://substackcdn.com/image/fetch/$s_!Z7FY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5ea21ccc-90aa-4750-861d-eb48a6144608_176x176.png) min{power}Explorations in computing and robotics focused on power-efficiency and safety -- personal posts by Avik De, robotics Ph.D. and founderBy Avik De](<https://www.avikde.me?utm_source=substack&utm_campaign=publication_embed&utm_medium=web>)

[![](https://substackcdn.com/image/fetch/$s_!13Dp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb5a886fd-347d-4694-b670-0253975d2ba9_659x547.png)It Can Think!Robotics and AI; the future we're building and how we'll get thereBy Chris Paxton](<https://itcanthink.substack.com?utm_source=substack&utm_campaign=publication_embed&utm_medium=web>)

## Trends in Robotics and AI

### 1) Commoditization

Going back to 2013, Avik’s Ph.D. research included the development of an internal research robot, Minitaur:

[![](https://substackcdn.com/image/fetch/$s_!4P2l!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c9a075c-f936-4270-8785-4812da0b85e4_956x680.png)](<https://substackcdn.com/image/fetch/$s_!4P2l!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c9a075c-f936-4270-8785-4812da0b85e4_956x680.png>)

It took a lot of (Ph.D. student) effort to build the infrastructure, but resulted in a unique development platform that was easy to program (as an Arduino), lightweight and relatively safe (5 kg), and capable of producing very agile and exciting-looking behaviors. There was nothing like it that you could buy. All in all, this endeavor to develop a new robot led to [papers](<https://www.avikde.me/p/vertical-hopper-compositions>), cool movies to show in talks, and even [a startup company](<https://www.ghostrobotics.io/>).

In the decade after, four-legged robots started to get out of the research lab and into public consciousness. The show Silicon Valley had a [Boston Dynamics Spot cameo in 2016](<https://www.businessinsider.com/silicon-valley-google-spot-robot-2016-4>), and robot videos designed to appeal to a broad audience, like [dancing](<https://www.youtube.com/watch?v=kHBcVlqpvZ8>), started to appear. Four-legged robots were officially out of the lab and in the wild, and this led to increased expectations for what they should do. Stably walking around used to be cutting edge, but became table stakes. Expectations for specs such as reliability, battery life, compute capability, ruggedness drove designs to be more complex. It became much more difficult for a couple of researchers with minimal engineering experience to put together a new robot. Moreover, after Chinese company Unitree entered the market and [dropped the asking price by almost 30x](<https://kr-asia.com/unitree-robotics-develops-personal-robot-dogs-that-jog-alongside-you>) in 2021, it became not worth the time and dollars to even try.

**The pre-paradigm period of lab-developed robotic hardware is being replaced by algorithm development for commoditized hardware.**

We have seen this play out in several robotics research labs. DJI commoditized consumer drones aggressively from 2013 onward, making it hard to justify custom builds even for capability reasons. By the mid-2010s, labs doing serious flight research (e.g., [Davide Scaramuzza’s group](<https://rpg.ifi.uzh.ch/people_scaramuzza.html>) at University of Zurich) were exclusively using commercial platforms. ETH Zurich’s [Robotic Systems Lab](<https://rsl.ethz.ch/research/researchtopics/legged-locomotion.html>) (which built ANYmal originally, and also STarLETH) now deploys their locomotion research on the ANYmal platform rather than building new hardware. [Boston Dynamics has an article](<https://bostondynamics.com/blog/what-makes-an-effective-research-robot/>) that talks about how commercial platforms let researchers hit the ground running.

Post-commoditization, researchers who want to demonstrate _algorithms_ working on robots can reap the benefits. Humanoid research circa 2015 meant figuring out “how do we actually build these things and make them not fall over,” whereas post-commoditization, time can be spent on higher-level algorithms and methods — we refer to this phenomenon as “**moving up the stack**.”

A secondary effect of commoditization is that _parts_ are now easier to get, and researchers can put together novel modular combinations of more mature components. The WidowX 250 Dynamixel-based arm from Trossen Robotics has become the default low-cost manipulation platform because it is cheap (~$3k) and can be used to create “leader-follower” setups for data collection. The [ALOHA paper](<https://arxiv.org/abs/2304.13705>) notes that the whole system with two arms costs ~$20k off-the-shelf. More recently, we have seen [robots like the YOR](<https://yourownrobot.ai/>) assembled from off-the-shelf parts for research purposes. This effect enables new types and form-factors of robots to be built — _we will return to this in the next section_.

The same trend applies to non-hardware **AI research**. Frontier language models cannot really be trained by academic research labs any more — research in these areas moves to fine-tuning commercial models instead. The following plots [were generated from arXiv data](<https://github.com/avikde/robo-research-trends>) and confirm these trends toward pretrained model usage in research compared to building them from scratch.

[![](https://substackcdn.com/image/fetch/$s_!Ry1_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d0c81fa-2963-4f6d-aa12-9f030a92a603_600x450.png)](<https://substackcdn.com/image/fetch/$s_!Ry1_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d0c81fa-2963-4f6d-aa12-9f030a92a603_600x450.png>)

[![](https://substackcdn.com/image/fetch/$s_!VfeU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F37f67c01-9553-4d2c-9903-15f7106bddea_600x450.png)](<https://substackcdn.com/image/fetch/$s_!VfeU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F37f67c01-9553-4d2c-9903-15f7106bddea_600x450.png>)

The Qwen series of models by Alibaba have nearly taken over the research world by facilitating fine-tuning. In 2026, no academics would think of training their own language models or even vision-language models from scratch — why would you, when Qwen 3.5 can already beat anything that’s within reach of an ordinary academic lab?

Just like for robotics hardware, **the pre-paradigm period of lab-developed models is being replaced by fine-tuning commercial models**.

Here as well, there are research ideas which can be pursued by **moving up the stack** : agentic reasoning, reinforcement learning, world representations, novel model architectures, etc. Robotics models are not like language models; there are fewer real world benchmarks and it seems that even within the domain of end-to-end deep learning there are plenty of ideas left unexplored.

### 2) Architectural Convergence

Labs used to have a narrower focus where they could carve their niche, e.g. computer vision, legged locomotion, etc. However, for a robot to demonstrate complex sensorimotor tasks, you need [all of the Sense-Plan-Act functions implemented in some way](<https://open.substack.com/pub/minpower/p/the-architecture-behind-end-to-end>). If you subscribe to the bitter lesson, even the best computer vision algorithm, when connected using hand-crafted interfaces to a planner and other downstream systems, cannot compete with end-to-end systems. General-purpose manipulation / locomotion research is [converging on behavior cloning and VLAs](<https://itcanthink.substack.com/p/interesting-directions-in-vision>) since it works well enough across many tasks, and performance improves with larger models and more data.

[![](https://substackcdn.com/image/fetch/$s_!qAhH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5518ef64-6a10-4f1d-8017-ddd845e0988b_1472x944.png)](<https://substackcdn.com/image/fetch/$s_!qAhH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5518ef64-6a10-4f1d-8017-ddd845e0988b_1472x944.png>)Behavior cloning with VLAs (source: [Physical Intelligence](<https://www.pi.website/research/human_to_robot>))

This trend has pushed many previously-diverse labs toward developing end-to-end models, which is a significant reduction in the diversity and richness in the research ecosystem. For better or worse, we appear to solidly be in a **paradigm of behavior cloning with end-to-end models**.

This has several benefits for researchers: they can build on existing work easily without re-inventing the wheel, and it creates a scaffolding for new contributions. However, it also has the side-effect of suppressing other schools of thought. In Kuhn’s somewhat ominous words,

> But there are always some men who cling to one or another of the older views, and they are simply read out of the profession, which thereafter ignores their work. The new paradigm implies a new and more rigid definition of the field. Those unwilling or unable to accommodate their work to it must proceed in isolation or attach themselves to some other group.

How do research labs and out-of-paradigm ideas stand out in the face of homogenization and consolidation in this paradigm? We discuss what we can learn from computer engineering in the next section.

[Subscribe now](<https://www.avikde.me/subscribe?>)

## What we can learn from Computer Engineering

By necessity, computer engineering has always been a bit ahead of the same technology curve as robotics. After all, we needed the chips to facilitate computations needed for robots to work.

We saw there a similar **commoditization** trend, with hardware complexity outgrowing what a research lab could build. The initial university fab era was anchored by [DARPA’s VLSI Project](<https://en.wikipedia.org/wiki/VLSI_Project>), which produced BSD Unix, the RISC concept, and MOSIS (a shared fab for academia). Once that era ended, academic research pivoted to what could be done without a fab.

As a response, computer engineering therefore shows a good set of examples of **moving up the stack** (transistors → meta-design tools and ISAs). Circa 2010, rather than building chips, Krste Asanović’s group at Berkeley [designed the open RISC-V ISA](<https://people.eecs.berkeley.edu/~krste/papers/EECS-2014-146.pdf>) explicitly motivated by the problem of proprietary architectures impeding academic research. With [Chisel](<https://github.com/chipsalliance/chisel>) (Berkeley), academics built better tools for designing chips, by expressing hardware designs in a high-level language, and it became the foundation for most RISC-V implementations.

In addition, CPU architectures converged to x86 for desktop and ARM for mobile because they worked well enough for most workloads, and design costs could be amortized across different applications — a **general-purpose computing paradigm**.

[![](https://substackcdn.com/image/fetch/$s_!Ncaw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19335b79-16cb-45ea-89b5-3274e08984e3_1022x690.png)](<https://substackcdn.com/image/fetch/$s_!Ncaw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19335b79-16cb-45ea-89b5-3274e08984e3_1022x690.png>)Performance saturation from the end of Dennard scaling (source: H&P 2017 lecture).

[Hennessy and Patterson’s 2017 Turing Award lecture](<https://dl.acm.org/doi/10.1145/3282307>) argued that the post-Dennard-scaling era opens up a new window for research in domain-specific accelerators, where the design space is exploratory again. Coincident with the success of deep neural networks, the last few years have seen a [Cambrian explosion in AI accelerators](<https://thechipletter.substack.com/p/ai-accelerators-the-cambrian-explosion>), ushering in much more innovation in computer architecture and silicon than was possible in CPUs.

In other words, computer engineering’s paradigm shift resulted in **domain-specific diversification.**

How do these apply to robotics and AI?

Just as chip fabrication leaving academia didn’t end computer architecture research, robotics research will find a home in core algorithms, training methodologies, and novel architectures**.** While papers can continue to be written on new methods and algorithms, unfortunately, the flashy demonstrations (important for fundraising and PR) may go out of lab reach. Similar to how ChatGPT capitalized on published transformer research, companies will capitalize on published public-domain research. It may become crucial to have a credit mechanism for academics for commercial usage of their work (this is not covered by academic metrics such as h-index).

The largest robotics companies are converging on general-purpose humanoids, optimizing for the broadest possible applicability and commercial value. By analogy to computer engineering’s **domain-specific diversification** , the next productive frontier for academic labs may be task-specific robots: surgical, agricultural, soft robots, etc., which diverge enough from general-purpose designs to make bespoke solutions worthwhile. A positive side-effect of the commoditization of hardware components (like actuators, IMUs, perception systems like the Kinect) all come together to facilitate this kind of development.

## The Future

While the external perception of robotics and AI research is that we are undergoing a revolution today, the internal view is more consistent with _commoditization_ and _convergence_. This paradigm has had a lot of positive side-effects, like establishing a framework and shared infrastructure, but also some serious downsides, like stifling research that doesn’t fit the mold. 

In response, we already see the reality of robotics research **moving up the stack** , and we will potentially begin to see examples of **domain-specific diversification** if the largest companies with the largest datasets corner the end-to-end behavior cloning approach.

Beyond that, it’s too early to predict if there is a paradigm shift coming. Kuhn says on this topic:

> Sometimes a normal problem, one that ought to be solvable by known rules and procedures, resists the reiterated onslaught of the ablest members of the group within whose competence it falls. On other occasions a piece of equipment designed and constructed for the purpose of normal research fails to perform in the anticipated manner, revealing an anomaly that cannot, despite repeated effort, be aligned with professional expectation.

[![](https://substackcdn.com/image/fetch/$s_!YrAc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F116dcd4e-6c38-4f02-88c6-c2b237be5d36_233x229.png)](<https://substackcdn.com/image/fetch/$s_!YrAc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F116dcd4e-6c38-4f02-88c6-c2b237be5d36_233x229.png>)Kuhn cycle ([source](<https://www.thwink.org/sustain/glossary/KuhnCycle.htm>))

Will there be a “piece of equipment” or “normal problem” whose unexpected result paves the way for the next robotics revolution? Optimistically, it seems like the current paradigm still has legs for a little while longer, but there is already work at the fringes looking toward the next set of leaps, like world model research, neuromorphic computing, etc. We’ll be writing about these topics over the coming weeks and months; stay tuned!

[Subscribe now](<https://www.avikde.me/subscribe?>)

 _If you enjoyed this post, please like (❤️) and restack — it helps others find my writing. Subscribe to receive new posts. All of this is greatly appreciated._

1

While originally intended for scientific fields, the [idea has been extended](<https://www.sciencedirect.com/science/article/abs/pii/0048733382900166>) to broader technological fields.
