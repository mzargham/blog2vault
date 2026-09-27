---
title: "Robots That Lift Heavy Things Must Cover Their Faces"
subtitle: "Spec sheets optimize for lifting, not looking human when you run"
date: 2026-09-24
slug: robots-that-lift-heavy-things-must
canonical_url: "https://www.avikde.me/p/robots-that-lift-heavy-things-must"
topic: "Uncategorized"
concepts:
  []
source: Substack
author: Avik De
---

# Robots That Lift Heavy Things Must Cover Their Faces

![](https://substackcdn.com/image/fetch/$s_!MhCu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d2b130a-eb28-483b-87e6-6fafe7ca7efe_1151x701.png)

*Spec sheets optimize for lifting, not looking human when you run*

> Originally published: [2026-09-24](https://www.avikde.me/p/robots-that-lift-heavy-things-must)

**Citations:** [[citations/en-wikipedia-org|en.wikipedia.org]] · [[citations/globaltimes-cn|globaltimes.cn]] · [[citations/robotlar-org|robotlar.org]] · [[citations/arxiv-org|arxiv.org]] · [[citations/figure-ai|figure.ai]] · [[citations/github-io|github.io]] · [[citations/journals-biologists-com|journals.biologists.com]] · [[citations/rai-inst-com|rai.inst.com]] · [[citations/science-org|science.org]]

---

The X-Humanoid Tien Kung Omni robot won the “small” category 400m race in the [World Humanoid Robot Games (WHRG)](<https://en.wikipedia.org/wiki/World_Humanoid_Robot_Games>) held in Beijing in August 2026. (Un)fortunately, its performance achievements have been somewhat overshadowed by its now-viral running gait:

> Rather than swinging its arms forward and back as a human sprinter does, the robot ran with its center of gravity pitched forward and its arms held high near its face, swinging them widely as its hips rotated from side to side — a gait viewers likened to “a shy person hiding behind their hands.” — _[Global Times](<https://www.globaltimes.cn/page/202608/1368875.shtml>)_

While it looked ridiculous, the [child-sized robot](<https://www.robotlar.org/en/humanoid-robots/xhumanoid-tien-kung-omni>) was quite fast, completing 400 meters in 45.66 seconds (near the men’s and women’s 400 m records).

In this article, I wanted to look at the reasons why the Omni robot runs like that. Should other robots run this way? Should people run this way?

There are actually a number of factors affecting these answers, some of them quite unintuitive. Let’s dig in! 

Thanks for reading! Subscribe for free to receive new posts and support my work.

## Two Popular Paths for RL Robot Locomotion

The behavior in the video above was developed with an algorithm that [appears frequently in this blog](<https://www.avikde.me/p/the-loops-and-hierarchies-of-embodied>): reinforcement learning (RL). An RL agent executes a _policy_(which you can think of as a deterministic set of rules by which it generates actions), and during training, it learns this policy by repeatedly interacting with the environment to maximize a reward. In most cases, the developer will set up the environment and specify the reward in a simulator, and the algorithm will step through the simulator (with massive parallelization) to develop the policy.

RL has proven itself to be incredibly effective at various robot tasks, and in particular robot locomotion. In addition to increasingly reliable robot hardware, the commoditization of RL is a large contributor to the improvements in robot locomotion and [athletic feats](<https://www.avikde.me/p/honors-humanoid-ran-the-fastest-half>) we have seen in the recent past.

RL’s weakness is that the task and the environment are locked in at training time, and cannot easily generalize at runtime — unexpected or “out of distribution” settings can cause unpredictable results. However, that limitation was moot for the humanoid robot games. The physical layout and sequence of obstacles on the course were predefined by the event organizers, and developers could recreate it in simulation and train the algorithm to work toward the goal. The WHRG was basically a perfect application for RL tools!

Some of the earliest RL locomotion in simulated environments appeared in 2017 [from DeepMind](<https://arxiv.org/abs/1707.02286>). As the paper’s results themselves state, the resulting “locomotion styles are idiosyncratic:”

As you can see, RL producing strange running gaits is nothing new! But why does it do that?

Remember that the agent is just trying to get its reward, and all the arm flails are goal-directed in order to obtain the reward from the simulation. If there is a persistent quirk in the simulator, robot dynamics, or environment, the RL agent will exploit it!

How do you “fix” this?

A popular second path for RL is to incorporate data of animal movement, which looks “natural” to us.

For example, [Figure AI](<https://www.figure.ai/news/reinforcement-learning-walking>) says (March 2025):

> A policy learned using RL might converge to sub-optimal control strategies that do not capture the stylistic attributes that define human walking. This includes walking with a human-like gait, with heel-strikes, toe-offs and arm-swing synchronized with leg movement. We inject this preference into our learning framework by rewarding the robot to mimic human walking reference trajectories. These trajectories establish a prior over the walking styles the policy is allowed to generate, while additional reward terms optimize for velocity tracking, power consumption and robustness to external perturbations and variations in terrain.

There is a long line of research showing how this can be done, ranging from methods that force strong adherence to the reference trajectories, to methods that more loosely learn to discriminate locomotion “style” preferences ([Adversarial Motion Priors](<https://arxiv.org/html/2104.02180v2>)).

[![](https://substackcdn.com/image/fetch/$s_!5c8J!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9ae5d904-8637-4547-9344-9411514951d4_3700x448.png)](<https://substackcdn.com/image/fetch/$s_!5c8J!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9ae5d904-8637-4547-9344-9411514951d4_3700x448.png>)Motions generated by [Adversarial Motion Priors (AMP)](<https://xbpeng.github.io/projects/AMP/index.html>)

All variants of these methods have the goal of making robot motions more natural or aesthetic by incorporating animal data. They also make the RL problem easier in some ways by making the reward easy to specify — just track the motion!

Then why didn’t the Omni robot do this as well?

[Subscribe now](<https://www.avikde.me/subscribe?>)

## The Two Paths in Conflict

The developers at [X-Humanoid told the Global Times](<https://www.globaltimes.cn/page/202608/1368875.shtml>):

> "We initially designed Tien Kung Omni's gait around a human-style arm swing," Han Gang, a motion control algorithm expert at the company, told the Global Times. In a simulated learning environment, the team gave the robot continuous rewards, and through repeated iteration on the data it gradually settled into a posture that suited it better. "It feels that this is more comfortable," Han said.

The reward and the “natural motion” expectations were at odds. 

This has also been covered in [published research](<https://arxiv.org/abs/2604.19102>). The researchers found that using Adversarial Motion Priors (AMP) is great for enforcing normal, human-like walking. However, those human-like style constraints over-constrains the neural network during highly dynamic tasks (like sprinting or jumping), and they present a method to effectively disable.

Is this tradeoff unavoidable?

## Back to Basic Physics

Let’s first look at why human runners swing their arms in what we might think of as the “expected” way.

As covered in this [JEB paper](<https://journals.biologists.com/jeb/article/217/14/2456/12120/The-metabolic-cost-of-human-running-is-swinging>),

> [T]he primary function of arm swing during distance running is to counterbalance the angular momentum generated by the swinging legs about the vertical axis.

Going further, the paper shows that swinging the arms the way we do is energetically more efficient than a number of other options (and I’d expect also the “face-covering” swing).

[![](https://substackcdn.com/image/fetch/$s_!wRXt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa22c64a0-f30b-415a-b0e7-0c6558fa2b0e_1114x646.jpeg)](<https://substackcdn.com/image/fetch/$s_!wRXt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa22c64a0-f30b-415a-b0e7-0c6558fa2b0e_1114x646.jpeg>)Not swinging the arms has a metabolic cost ([source](<https://journals.biologists.com/jeb/article/217/14/2456/12120/The-metabolic-cost-of-human-running-is-swinging>))

So, we swing our arms to compensate for the angular momentum imparted by our legs swinging and keep our torso stable.

But Physics applies the same way to the robot; something needs to compensate for its swinging legs! Unfortunately, here the Omni robot runs into a problem:

> Swinging the arms rapidly places a heavy load on the shoulder joints, which can cause them to heat up and drive up energy consumption — leaving the robot unable to sustain the full 400m. Running with its hands near its face allows the robot to complete the distance quickly while keeping its legs powerful and its arms under low load. — _Global Times article_

That is a bit difficult to understand, but I think I can explain what might have been going on. I don’t have any information about the Omni’s design parameters, so the following paragraph is purely hypothetical.

If the robot’s shoulder joints have been designed to statically hold objects (manufacturers like to advertize how much weight it can carry), they likely have high inertia (heavily geared). I [covered in a previous article](<https://www.avikde.me/p/honors-humanoid-ran-the-fastest-half>) that robot joints with high inertia will generate less heat to produce torque statically (all else being equal). Unfortunately, when dynamically moving back and forth, the high inertia will cause them to require more torque to accelerate, and generate _more_ heat. This would cause the shoulder joint to overheat (as the article quote says), leading to a preference for a different motion for angular momentum compensation. The pitched-forward, yawing torso accomplishes just that, while keeping the shoulder motion to a much smaller amplitude.

[Subscribe now](<https://www.avikde.me/subscribe?>)

This hypothetical applies beyond our Omni robot case study: a [recent project at RAI](<https://rai-inst.com/resources/blog/bimanual-robot-for-dynamic-manipulation/>) goes deeper into upper arm design, showing a plot of how conventional robot arms tend to have significantly higher inertia than human arms:

[![Multi-panel figure, panels A through C, combining two-dimensional contour line plots, labeled computer renderings of robot arms, color-mapped arm models with a color scale bar, and a box-and-whisker plot. AI generated, human reviewed. \[AI\]](https://substackcdn.com/image/fetch/$s_!wumF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa152482b-f0e5-477a-8a18-3d14a978b5ed_1396x1569.jpeg)](<https://substackcdn.com/image/fetch/$s_!wumF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa152482b-f0e5-477a-8a18-3d14a978b5ed_1396x1569.jpeg>)“Effective mass” (similar to inertia) of human arms compared to typical robot arms ([source](<https://www.science.org/doi/10.1126/scirobotics.aee1868>))

This is a classic mismatch in what the joint was designed to do, and what it ended up being used for.

[![](https://substackcdn.com/image/fetch/$s_!MhCu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d2b130a-eb28-483b-87e6-6fafe7ca7efe_1151x701.png)](<https://substackcdn.com/image/fetch/$s_!MhCu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d2b130a-eb28-483b-87e6-6fafe7ca7efe_1151x701.png>)Omni with compact shoulder joints (left) and AthenaZero with bulky shoulder joints (right)

When robot designs are drawn up, people assume that the function of the arms is to pick up and carry objects. For winning spec sheet battles, it is tempting to enable it to carry heavier objects, resulting in compact, high-inertia shoulder joints.

But arms serve other purposes (including, but not limited to, counterbalancing leg swing) that may be impacted by optimizing them for carrying. [Once again](<https://www.avikde.me/p/honors-humanoid-ran-the-fastest-half>), we come to see that engineering often has more to do with choosing the best trade-off than the execution.

My other takeaway is about comparing robots to animals. Even though it looks like human running records don’t stand a chance against running robots any more, biological _adaptability_ hasn’t been matched yet. People can run, carry, and even train themselves to do these things better, while robots that want to lift heavy weights seem to need to cover their faces while running!

_Thanks for reading! If you enjoyed this post, please like (❤️) and restack — it helps others find my writing. Subscribe to receive new posts._

[ Share](<https://www.avikde.me/p/robots-that-lift-heavy-things-must?utm_source=substack&utm_medium=email&utm_content=share&action=share>)

[Subscribe now](<https://www.avikde.me/subscribe?>)

## Further Reading

The relationship between leg inertia and running gait:

How to design fast and efficient running robots:
