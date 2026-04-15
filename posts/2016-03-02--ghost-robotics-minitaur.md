---
title: "Ghost Robotics and Minitaur"
subtitle: "Research to startup"
date: 2016-03-02
slug: ghost-robotics-minitaur
canonical_url: "https://www.avikde.me/p/ghost-robotics-minitaur"
topic: "Quadrupedal Robot Development"
concepts:
  - "Feedback Loops"
  - "BLDC Actuators"
  - "Direct Drive Design"
  - "Impedance Control"
  - "Quadrupedal Locomotion"
  - "Research Commercialization"
source: Substack
author: Avik De
---

# Ghost Robotics and Minitaur

![](https://substackcdn.com/image/youtube/w_728,c_limit/bnKOeMoibLg)

*Research to startup*

> Originally published: [2016-03-02](https://www.avikde.me/p/ghost-robotics-minitaur)

**Topic:** [[topics/quadrupedal-robot-development|Quadrupedal Robot Development]]
**Concepts:** [[concepts/feedback-loops|Feedback Loops]] · [[concepts/bldc-actuators|BLDC Actuators]] · [[concepts/direct-drive-design|Direct Drive Design]] · [[concepts/impedance-control|Impedance Control]] · [[concepts/quadrupedal-locomotion|Quadrupedal Locomotion]] · [[concepts/research-commercialization|Research Commercialization]]
**Citations:** [[citations/ghostrobotics-io|ghostrobotics.io]] · [[citations/ieeexplore-ieee-org|ieeexplore.ieee.org]] · [[citations/kodlab-seas-upenn-edu|kodlab.seas.upenn.edu]]

---

Part of the reason for the long hiatus from posting is that I’ve been supremely busy with a few things. One of them is that I’ve cofounded a robotics company – [Ghost Robotics](<http://www.ghostrobotics.io/>)!

[![](https://substackcdn.com/image/fetch/$s_!cvb0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0242e0ce-c83a-4abe-8961-bcfa9653996f_309x108.png)](<https://substackcdn.com/image/fetch/$s_!cvb0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0242e0ce-c83a-4abe-8961-bcfa9653996f_309x108.png>)

You’re probably wondering what the name is about. One of the main things that sets our actuators apart is that they are _transparent_. No, that doesn’t mean that you can see through them, but rather that the motors can feel forces applied on them by the world. This is important, for things like reacting to perturbations, like when the robot leg touches the ground (demo of that in the gif below), or for safety if the motors are running near humans. And, well, ghosts are transparent?

Thanks for reading min{power} by avikde! Subscribe for free to receive new posts.

### **Minitaur**

The robot that I’ve spent most of my time working on since last summer is called Minitaur. We’ve written one journal paper about its design and [the open-access preprint is now up](<http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7403902>).

Official Ghost video:

The video above got picked up by a lot of media (at least for the time for Ghost Robotics). However, everyone does now assume our robots can climb fences, so maybe we shouldn’t have put that so out there.

### Direct-drive design paper

The paper1 initially disclosing Minitaur, which is to date my highest-cited paper, describes two key aspects of its design.

  * The unique leg design, which optimized mechanical advantage for vertical jumping from a squatting position

  * The electromechanical architecture, that led to us creating a whole family of new robots in [Kod*lab](<https://kodlab.seas.upenn.edu/>). This kind of cambrian explosition in new robots was unheard of in the early 2010’s, when complex and high-power robotic actuators and controllers were not nearly as easy to develop. I remain quite proud that both Minitaur (within UPenn and elsewhere) and the Jerboa were key to the development of a number of research projects and publications, which I’ve written about in other posts.




[![](https://substackcdn.com/image/fetch/$s_!gT8e!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe1a0c5c6-d1f1-47f6-8b11-9c4dcd991cb5_809x183.png)](<https://substackcdn.com/image/fetch/$s_!gT8e!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe1a0c5c6-d1f1-47f6-8b11-9c4dcd991cb5_809x183.png>)A family portrait of a few of the robots developed from the Minitaur and Jerboa electromechanical architecture.

### Some of my own clips from 2016

These clips show the initial behaviors we put together, with the help of Turner Topping, to demonstrate the Minitaur hardware. I’ve linked below my article about the more in-depth paper about the approach to developing these simple behaviors, which were all controlled by an on-board microcontroller.

[![](https://substackcdn.com/image/fetch/$s_!Wp6p!,w_1456,c_limit,f_auto,q_auto:good,fl_lossy/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faecf23e4-f598-44cf-957c-d60f52ceccc5_600x338.gif)](<https://substackcdn.com/image/fetch/$s_!Wp6p!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faecf23e4-f598-44cf-957c-d60f52ceccc5_600x338.gif>)

Also see 

1

[Design principles for a family of direct-drive legged robots](<https://scholar.google.com/citations?view_op=view_citation&hl=en&user=m-A4ZdEAAAAJ&sortby=pubdate&citation_for_view=m-A4ZdEAAAAJ:2VqYfGB8ITEC>)
