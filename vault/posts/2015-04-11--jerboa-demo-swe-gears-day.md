---
title: "Jerboa demo for SWE gears day"
subtitle: "Robotics research meets outreach"
date: 2015-04-11
slug: jerboa-demo-swe-gears-day
canonical_url: "https://www.avikde.me/p/jerboa-demo-swe-gears-day"
tags:
  - research
concepts:
  - "Tail"
source: Substack
author: Avik De
---

# Jerboa demo for SWE gears day

![](https://substackcdn.com/image/youtube/w_728,c_limit/4bsEIXvLJVI)

*Robotics research meets outreach*

> Originally published: [2015-04-11](https://www.avikde.me/p/jerboa-demo-swe-gears-day)

**Topics:** [[topics/research|Research]]
**Concepts:** [[concepts/tail|Tail]]
**Citations:** [[citations/fling-seas-upenn-edu|fling.seas.upenn.edu]]

---

Doing robotics research is one thing, making them presentable and accessible to the public is quite another. I was tasked with engaging high school girls (who were getting a GRASP lab tour for [SWE GEARS Day](<https://fling.seas.upenn.edu/~swe/cgi-bin/gearsday.php>)), and I’d guess that keeping their attention through a robot presentation is probably much harder than a conference talk audience’s.

The other challenge was that the Jerboa behaviors I’ve mostly [worked on so far](<http://avikde.me/jerboa-hopping-video/>) are relatively high-energy and require a boom, and it isn’t very practical to demo something like that. I quickly threw together (in the few hours I had to prepare) a Buehler clock leg trajectory (feedforward, clocked), where I had the option of choosing a leg phase offset of 0 (legs together, or “hopping”) or 0.5 (legs out of phase, or “walking”).

It worked in a basic sense, but I learned that turning needs a lot more attention than I put into it if you’re going to do a demo. _This is a lesson for all you roboticists content to be working in the sagittal plane!_ I’ll describe the hacks that went into putting this together (they only worked moderately), but here’s a video first:

### **Turning**

The first thing I tried is ironically the one thing that _requires_ that you not think of the motors as position servos (as is done on RHex in the basic use cases)–lowering the proportional gain on the inside leg and stiffening the one on the outside. This actually worked decently (before the demo itself–evidence of failures above). I think the idea itself is sound, but the loosening I did might have been a tad too agressive.

### **Tail motion in walking**

When the legs are out of phase, there is significant body roll each half-step because of gravity acting through the CoM (offset from the leg contact point). The idea was that the tail might exert counter-moments from the normal reaction at the leg contact point, and quasistatically moving the tail away from the stance leg would help.

I think we are going to examine similar ideas in much more depth over the summer, so I won’t give much away about what worked and didn’t now, but perhaps soon I’ll post logs of body roll vs. different tail yaw phasing choices.
