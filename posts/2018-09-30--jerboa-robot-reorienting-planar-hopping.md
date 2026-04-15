---
title: "Jerboa robot reorienting, planar hopping, and hip-hop"
subtitle: "Follow-on projects with the Penn Jerboa robot from 2016-2018"
date: 2018-09-30
slug: jerboa-robot-reorienting-planar-hopping
canonical_url: "https://www.avikde.me/p/jerboa-robot-reorienting-planar-hopping"
topic: "Jerboa Robot Development"
concepts:
  - "3D Locomotion"
  - "Direct-Drive Motors"
  - "Tailed Reorientation"
source: Substack
author: Avik De
---

# Jerboa robot reorienting, planar hopping, and hip-hop

![](https://substackcdn.com/image/youtube/w_728,c_limit/vxgkAOdeP1Y)

*Follow-on projects with the Penn Jerboa robot from 2016-2018*

> Originally published: [2018-09-30](https://www.avikde.me/p/jerboa-robot-reorienting-planar-hopping)

**Topic:** [[topics/jerboa-robot-development|Jerboa Robot Development]]
**Concepts:** [[concepts/3d-locomotion|3D Locomotion]] · [[concepts/direct-drive-motors|Direct-Drive Motors]] · [[concepts/tailed-reorientation|Tailed Reorientation]]
**Citations:** [[citations/en-wikipedia-org|en.wikipedia.org]] · [[citations/mit-edu|mit.edu]]

---

I have previously introduced the Penn Jerboa robot, developed ~2014 at UPenn.

While it was technically the first of the “family of direct-drive robots” developed during my Ph.D., the first paper that was published on the architecture featured Minitaur, as I wrote here:

Minitaur had 8 motors and 4 legs—which made it signficantly easier to program to jump, hop, walk—and so it was fair enough that it was featured in the first publication on these robots, and went on to be the first “product” that was spun out.

Nevertheless, Jerboa was morphologically significantly more interesting, and became the topic and motivation for several new directions of research. In this article, I’ll talk about a few of them that were completed during my tenure, though there were projects underway as recently as 2025.

Thanks for reading min{power}! Subscribe for free to receive new posts and support my work.

### Tailed reorientation (2016)

While most of my doctoral research had to do with walking and running using legs, in this project, we looked purely at re-orienting (like a falling cat) using a tail. This implied a few key differences from the previously discussed mobility research:

  1. We only need to analyze a continuous dynamical system without any mode switching, i.e. it is not a [hybrid](<https://open.substack.com/pub/minpower/p/hybrid-averaging?utm_campaign=post-expanded-share&utm_medium=web>) dynamical system

  2. The inputs (or actuators) available are the ones connected to the robot tail

  3. The objective function is very simple - get the main body/torso orientation to a desired state




The Jerboa robot had the tail connected to two motors, with a transmission that meant that the torque produced in the tail actuators was larger than from the legs (core stronger than legs):

[![](https://substackcdn.com/image/fetch/$s_!Nx42!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf5e8b6e-f6ba-4ecc-a06d-907a4e3490ba_853x343.png)](<https://substackcdn.com/image/fetch/$s_!Nx42!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf5e8b6e-f6ba-4ecc-a06d-907a4e3490ba_853x343.png>)Jerboa robot doubly actuated tail

There are a number of similarities to the [falling cat problem](<https://en.wikipedia.org/wiki/Falling_cat_problem>), except that cats are predominantly using their core muscles, and flexibility in their core/back instead of their tails for reorienting while falling.

As the paper1 shows, the mathematical analysis is satisfying and can be verified experimentally while free-falling, or during the aerial phase of hopping.

In both the falling cat problem and this one, the key effect is that there is a [non-holonomic constraint](<https://en.wikipedia.org/wiki/Nonholonomic_system>) on the system dynamics due to the conservation2 of angular momentum. An easy to understand analogy is parallel parking a car: there are no inputs that can translate a car sideways, but a driver is able to use the steering and fore-aft inputs to move into a parking spot alongside.

### Pitch-unlocked hopping (2018)

The initial Jerboa hopping results constrained the pitch of the body using a “boom” (the large carbon fiber tube visible in the video):

This is because it was difficult enough to get “tail-energized” hopping to work, where a single actuator (“wagging” the tail") would controllably make the robot hop up and down as well as translate forward and back.

It took a few years to remove those guardrails and free the body pitch. After this project, there is still a carbon fiber tube, but it is only constraining the robot in a plane.3

The solution that we published4 was, of course, to add more bottom-up controllers working in parallel. This path had been clear since the initial Jerboa publication:

[![](https://substackcdn.com/image/fetch/$s_!vZnQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c997d46-e079-465e-8f98-13d24ca42ab0_500x182.png)](<https://substackcdn.com/image/fetch/$s_!vZnQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c997d46-e079-465e-8f98-13d24ca42ab0_500x182.png>)A cartoon schematic depicting that **(top)** when the Jerboa robot is in aerial or flight phase, the tail is used for stabilizing the orientation of the body, and **(bottom)** when it is on the ground, the tail wagging is used to jump back up by energizing the leg springs.

Still, a lot of work had to be done to optimize the tail and leg design, as described in the paper, and to tune the behavior:

### Hip-energized hopping “hip-hop” (unpublished)

As shown in the cartoon above, the initially-imagined Jerboa robot hopping behavior allocated5 control inputs to degrees of freedom as follows:

  * Tail in stance → height

  * Hip in stance → pitch & tail position (“shape”)

  * Tail in flight → pitch & tail position (“shape”)

  * Hip in flight → reposition leg




Is this the only “allocation”? One idea for an alternate was:

  * Tail in stance or flight → pitch & tail position (“shape”)

  * Hip in stance → height

  * Hip in flight → reposition leg




The key difference was that the legs would “power” the locomotion, which is an intuitive concept from the perspective of a tail-less animal. I developed some simple feedback controllers and showed in simulation that this could work, but it was very sensitive:

On the robot, the experiments were even more primitive, and I had to use the tail as a kick-stand to poke against the ground to stabilize the body pitch:

1

[Frontal plane stabilization and hopping with a 2DOF tail](<https://scholar.google.com/citations?view_op=view_citation&hl=en&user=m-A4ZdEAAAAJ&citation_for_view=m-A4ZdEAAAAJ:dBIO0h50nwkC>)

2

As an aside, this is a consequence of my favorite result from physics, [Noether’s theorem](<https://en.wikipedia.org/wiki/Noether%27s_theorem>).

3

There is a long tradition of “planar hoppers” constrained/supported as such, e.g. [Raibert’s planar hopper](<http://www.ai.mit.edu/projects/leglab/robots/2D_hopper/2D_hopper.html>).

4

[Jerboa design paper](<https://scholar.google.com/citations?view_op=view_citation&hl=en&user=m-A4ZdEAAAAJ&citation_for_view=m-A4ZdEAAAAJ:HtS1dXgVpQUC>)

5

This is once again inspired by Raibert’s “[control of hopping in three parts](<http://www.ai.mit.edu/projects/leglab/robots/3D_hopper/3D_hopper.html>).” Modern optimal control or learned methods will not have these allocations, instead leveraging all possible actuators at all times. Our idea during my thesis was to explicitly not do that, with the advantage of keeping controllers low-dimensional and modular. Does this make sense today as computation gets cheaper and more powerful, or is it pointless? Let me know in the comments!
