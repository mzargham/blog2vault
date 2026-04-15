---
title: "Lessons from AVs on safety in end-to-end pipelines"
subtitle: "Recent developments in autonomous vehicles on recognizing and handling distribution shift"
date: 2026-03-20
slug: lessons-from-avs-on-safety-in-end
canonical_url: "https://www.avikde.me/p/lessons-from-avs-on-safety-in-end"
topic: "End-to-End Robotics Pipelines"
concepts:
  - "World Models"
  - "End-to-End Robotics Pipelines"
  - "Control Systems"
source: Substack
author: Avik De
---

# Lessons from AVs on safety in end-to-end pipelines

![](https://substackcdn.com/image/fetch/$s_!8Xju!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21a8506d-3fba-41db-bafc-008bc52758a9_1600x804.jpeg)

*Recent developments in autonomous vehicles on recognizing and handling distribution shift*

> Originally published: [2026-03-20](https://www.avikde.me/p/lessons-from-avs-on-safety-in-end)

**Topic:** [[topics/end-to-end-robotics-pipelines|End-to-End Robotics Pipelines]]
**Concepts:** [[concepts/world-models|World Models]] · [[concepts/end-to-end-robotics-pipelines|End-to-End Robotics Pipelines]] · [[concepts/control-systems|Control Systems]]
**Citations:** [[citations/theverge-com|theverge.com]] · [[citations/electrek-co|electrek.co]] · [[citations/ruixu-us|ruixu.us]] · [[citations/arxiv-org|arxiv.org]] · [[citations/counterpointresearch-com|counterpointresearch.com]]

---

This short post covers a couple of recent updates from the autonomous vehicle (AV) industry with connections to broader and more general safety in robotics.

### Recognizing performance deterioration

This [Verge article from March 19](<https://www.theverge.com/transportation/897303/tesla-full-self-driving-nhtsa-probe-march-2026>) reports that there could be an impending recall of Tesla’s Full-Self Driving (FSD) service. I’m not interested in making any judgments about self-driving capability, but rather whether the root cause has anything we can learn from in broader robotics.

[![](https://substackcdn.com/image/fetch/$s_!KoIT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e8c97af-1c46-4e36-b5b0-17f23172671c_1246x498.png)](<https://substackcdn.com/image/fetch/$s_!KoIT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e8c97af-1c46-4e36-b5b0-17f23172671c_1246x498.png>)Source: The Verge article linked above. Emphasis mine.

The issue appears to be that the system **didn’t know when it wasn’t working well**(causing the issues in the NHTSA filing), or that it did and didn’t notify the driver (which is unlikely, so we’ll assume the former).

[![Tesla Full Self-Driving Beta 10.69 barrier](https://substackcdn.com/image/fetch/$s_!8Xju!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21a8506d-3fba-41db-bafc-008bc52758a9_1600x804.jpeg)](<https://substackcdn.com/image/fetch/$s_!8Xju!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21a8506d-3fba-41db-bafc-008bc52758a9_1600x804.jpeg>)Tesla FSD ([source](<https://electrek.co/2026/03/19/nhtsa-upgrades-tesla-fsd-visibility-investigation-3-2-million-vehicles/>))

This phenomenon isn’t isolated to AVs. The latest article in my Vision-Language-Action (VLA) robotics pipeline series went hands-on into [debugging one](<https://www.avikde.me/i/188827303/vla-debugging-ideas-and-techniques>), and while we found some techniques that can aid developers, they didn’t directly help at inference time. Item 1 in [Rui Xu’s candid post-mortem](<https://ruixu.us/posts/six-things-robotics-startup>) of K-Scale Labs mentions the pitfalls of trusting a “large model” vs. dedicated safety features. Recent papers on VLAs mention the fragility when moving away from the training distribution (e.g. [Fang et al Jun 2025](<https://arxiv.org/html/2506.09930v1>), [Hu et al Jan 2026](<https://arxiv.org/html/2512.16760v2>)).

### Potential solutions: redundancy, confidence, architecture

NVIDIA recently announced their new Alpamayo model and accompanying AV stack as a reference open model and toolchain. During the CES 2026 keynote, Jensen Huang said something intriguing about safety:

[![](https://substackcdn.com/image/fetch/$s_!MHGN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e20eb32-d24e-4ebc-89e5-6ca44eceb0a4_1464x776.png)](<https://substackcdn.com/image/fetch/$s_!MHGN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e20eb32-d24e-4ebc-89e5-6ca44eceb0a4_1464x776.png>)Source: [Junko’s Tech Probe article](<https://junkoyoshidaparis.substack.com/p/nvidia-pulling-an-elon-might-have>)

This parallel or hybrid architecture with a classical stack and a policy arbitrator were also covered in this [CounterPoint research article](<https://counterpointresearch.com/en/insights/counterpoint-conversations-nvidia-at-ces-from-full-stack-autonomy-to-an-open-ecosystem-play>). Interestingly, I can’t find references from NVIDIA themselves about this parallel system other than Jensen’s keynote — it’s possible it is just early in development.

A related approach is to have the VLA output some kind of confidence (vs. a separate “policy arbitrator”). [Zollo et al (Dec 2025)](<https://arxiv.org/pdf/2507.17383>) formalizes the problem of confidence calibration for VLA policies, describes how to extract confidence estimates from contemporary VLA architectures, and notes that current VLAs lack a reliable mechanism for quantifying the uncertainty of their chosen action sequences. It also introduces two potential remedies: prompt ensembles and action-wise Platt scaling.

Lastly, inserting some debuggable interfaces into end-to-end pipelines can facilitate inspection and safety — lower-level controllers can apply dedicated safety constraints based on the information passed down from a higher-level controller. This [appears to still be possible](<https://www.avikde.me/p/the-architecture-behind-end-to-end>) in most successful humanoid robotics demonstrations of today due to a combination of factors. Keeping that architectural feature around may have long-standing benefits, based on current events in the AV industry!

Thanks for reading! I have been working on the next part of the [end-to-end pipeline series](<https://www.avikde.me/p/the-architecture-behind-end-to-end>), with a deep dive into the action head and closed-loop behavior. If you liked this post, please share and subscribe.

Thanks for reading min{power}! Subscribe for free to receive new posts and support my work.
