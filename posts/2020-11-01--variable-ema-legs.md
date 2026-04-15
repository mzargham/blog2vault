---
title: "A 100mg hopping robot leg 'Nanotaur'"
subtitle: "Some unpublished results from the Harvard Microrobotics postdoc on a hopping robot leg with variable effective mechanical advantage"
date: 2020-11-01
slug: variable-ema-legs
canonical_url: "https://www.avikde.me/p/variable-ema-legs"
tags:
  - research
  - microrobotics
  - bio-inspired-locomotion
  - mechanical-transmission-design
  - multi-modal-locomotion
concepts:
  - "Robotics"
  - "Biomechanics"
  - "Mechanical Engineering"
  - "Variable Effective Mechanical Advantage"
  - "Five-Bar Linkage"
  - "Piezoelectric Actuation"
  - "Hopping Locomotion"
  - "RoboBee Architecture"
  - "Symmetric Joint Actuation"
source: Substack
author: Avik De
---

# A 100mg hopping robot leg "Nanotaur"

![](https://substackcdn.com/image/fetch/$s_!solN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe3233fd-9d6a-46d3-bc34-660957f5ae7b_382x311.png)

*Some unpublished results from the Harvard Microrobotics postdoc on a hopping robot leg with variable effective mechanical advantage*

> Originally published: [2020-11-01](https://www.avikde.me/p/variable-ema-legs)

**Topics:** [[topics/research|Research]] · [[topics/microrobotics|Microrobotics]] · [[topics/bio-inspired-locomotion|Bio Inspired Locomotion]] · [[topics/mechanical-transmission-design|Mechanical Transmission Design]] · [[topics/multi-modal-locomotion|Multi Modal Locomotion]]
**Concepts:** [[concepts/robotics|Robotics]] · [[concepts/biomechanics|Biomechanics]] · [[concepts/mechanical-engineering|Mechanical Engineering]] · [[concepts/variable-effective-mechanical-advantage|Variable Effective Mechanical Advantage]] · [[concepts/five-bar-linkage|Five-Bar Linkage]] · [[concepts/piezoelectric-actuation|Piezoelectric Actuation]] · [[concepts/hopping-locomotion|Hopping Locomotion]] · [[concepts/robobee-architecture|RoboBee Architecture]] · [[concepts/symmetric-joint-actuation|Symmetric Joint Actuation]]

---

During my post-doc, I got somehow close to merging the legged work on Minitaur during my Ph.D. with the piezoelectrically driven laminate RoboBee architecture of the Harvard Microrobotics lab.

I never got around to publishing this work, but I did built a two-joint symmetric five-bar leg. As with Minitaur, actuating the two joints could produce motion and force in the plane to be used for hopping.

[![](https://substackcdn.com/image/fetch/$s_!solN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe3233fd-9d6a-46d3-bc34-660957f5ae7b_382x311.png)](<https://substackcdn.com/image/fetch/$s_!solN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe3233fd-9d6a-46d3-bc34-660957f5ae7b_382x311.png>)“Nanotaur” leg

### Leg design and transmission for hopping

In addition, something else that was very interesting (regretfully not explored) was tuning the variable effective mechanical advantage using the transmission specifically for hopping (like we did for flapping in another paper):

  * When the leg was compressed (and presumably pushing against the ground for jumping), the actuators had high effective mechanical advantage.

  * When extended (presumed flying through the air), the actuators had lower mechanical advantage




[![](https://substackcdn.com/image/fetch/$s_!5TTu!,w_1456,c_limit,f_auto,q_auto:good,fl_lossy/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb80010b-d340-41f7-bf21-680e29e538ee_315x242.gif)](<https://substackcdn.com/image/fetch/$s_!5TTu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb80010b-d340-41f7-bf21-680e29e538ee_315x242.gif>)Driving the actuators in phase could produce a hopping motion, where the ground would be toward the right of the image. In addition, Leg compressed: high EMA <\----> Leg extended: low EMA.

The two actuators could also be driven out-of-phase for walking or jumping in a plane:

[![](https://substackcdn.com/image/fetch/$s_!E0dc!,w_1456,c_limit,f_auto,q_auto:good,fl_lossy/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20a4e229-ae1d-495b-89d7-26a1c16447c1_285x280.gif)](<https://substackcdn.com/image/fetch/$s_!E0dc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20a4e229-ae1d-495b-89d7-26a1c16447c1_285x280.gif>)Driven differently, we can get something resembling a walking gait pattern

### Hopping demonstration

[![](https://substackcdn.com/image/fetch/$s_!hssh!,w_1456,c_limit,f_auto,q_auto:good,fl_lossy/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4a75e37-59bd-4670-a452-41922bf7ebfd_290x235.gif)](<https://substackcdn.com/image/fetch/$s_!hssh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4a75e37-59bd-4670-a452-41922bf7ebfd_290x235.gif>)Supported by a boom, this little leg could indeed hop.

[![](https://substackcdn.com/image/fetch/$s_!C8mc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F12a09272-61bf-4cd9-bd41-27f6c2b7cf52_337x253.png)](<https://substackcdn.com/image/fetch/$s_!C8mc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F12a09272-61bf-4cd9-bd41-27f6c2b7cf52_337x253.png>)Log corresponding to the trial above, showing cycling vertical height, and estimated leg phase.

Compare to Jerboa vertical hopping:
