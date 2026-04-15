---
title: "Ph.D. thesis on modularity in robotics"
subtitle: "Defense completed"
date: 2017-09-15
slug: phd-defense
canonical_url: "https://www.avikde.me/p/phd-defense"
topic: "Modular Robotics Control Architecture"
concepts:
  - "Legged Locomotion"
  - "Control Decomposition"
  - "Parallel Composition"
  - "Actuator Allocation"
  - "Low-Dimensional Controllers"
  - "Optimal Control"
source: Substack
author: Avik De
---

# Ph.D. thesis on modularity in robotics

![](https://substackcdn.com/image/youtube/w_728,c_limit/l6p2a9SIy_o)

*Defense completed*

> Originally published: [2017-09-15](https://www.avikde.me/p/phd-defense)

**Topic:** [[topics/modular-robotics-control-architecture|Modular Robotics Control Architecture]]
**Concepts:** [[concepts/legged-locomotion|Legged Locomotion]] · [[concepts/control-decomposition|Control Decomposition]] · [[concepts/parallel-composition|Parallel Composition]] · [[concepts/actuator-allocation|Actuator Allocation]] · [[concepts/low-dimensional-controllers|Low-Dimensional Controllers]] · [[concepts/optimal-control|Optimal Control]]
**Citations:** [[citations/ai-mit-edu|ai.mit.edu]] · [[citations/kodlab-seas-upenn-edu|kodlab.seas.upenn.edu]] · [[citations/repository-upenn-edu|repository.upenn.edu]] · [[citations/cogneurosociety-org|cogneurosociety.org]]

---

I completed my Ph.D. at Penn on the topic of modularity in robotics. I have discussed this topic in a number of posts here.

### What does it mean?

One of the best ways to discuss that is in the context of this figure from the thesis1. It is showing how we create an allocation of actuators in different phases of motion to different control objectives for the Jerboa robot to hop.

[![](https://substackcdn.com/image/fetch/$s_!02a2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F16a66a36-55bd-4e20-97f1-eb41bc35da17_600x336.png)](<https://substackcdn.com/image/fetch/$s_!02a2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F16a66a36-55bd-4e20-97f1-eb41bc35da17_600x336.png>)Cartoon schematic describing allocation of actuators to control objectives for Jerboa robot hopping

As I [wrote previously](<https://www.avikde.me/p/jerboa-robot-reorienting-planar-hopping>), this is inspired by Raibert’s “[control of hopping in three parts](<http://www.ai.mit.edu/projects/leglab/robots/3D_hopper/3D_hopper.html>).” Modern optimal control or learned methods will not have these allocations, instead leveraging all possible actuators at all times. Our idea during my thesis was to explicitly not do that, with the advantage of keeping controllers low-dimensional and modular. 

Does this make sense today as computation gets cheaper and more powerful, or is it pointless? Let me know in the comments!

Thanks for reading min{power}! Subscribe for free to receive new posts and support my work.

The different controllers with different objectives run in parallel, so we termed this concept “parallel composition,” where the objects being composed are behavior primitives. The concept of motor primitives is drawn from neuroscience2, and our idea here was to develop complex robotic behaviors by synthesizing them from primitive ones.

Most of my thesis work was supported by a grant whose objective was to develop methods for “[programming work](<https://kodlab.seas.upenn.edu/research/programmingwork/>).” The usage of “programming” naturally draws comparisons to computing. This analogy is difficult on one hand, due to mechanical systems exhibiting real-world messiness of physics, but on the other hand, enticing to think about modularly snapping together aspects of robotic behavior to make new ones.

### Papers and defense

Using these ideas, we developed a method that generalizes across different morphologies (such as a hopping monoped, tailed biped, and a quadruped), to enable hopping, running, walking behaviors with empirical demonstrations and some analytical proofs.

Two of the main papers on this thread are discussed in other articles here:

Here is a poor-quality GoPro video of my defense:

I’m going to stay at Penn as a postdoc for a little bit while simultaneously [working with Ghost Robotics](</ghost-robotics-minitaur/>).

1

[Modular Hopping and Running via Parallel Composition](<https://repository.upenn.edu/entities/publication/10b266fd-41d2-49b6-ac90-0ee614bca00a>)

2

[Unraveling the Motor Movements That Connect All Primates - Cognitive Neuroscience Society](<https://www.cogneurosociety.org/primates_motor_kaas/>)
