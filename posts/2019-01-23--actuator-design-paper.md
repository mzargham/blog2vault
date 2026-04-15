---
title: "Task-based motor control algorithm design"
subtitle: "Paper in RAL 2019 about applying task-specifics to BLDC control"
date: 2019-01-23
slug: actuator-design-paper
canonical_url: "https://www.avikde.me/p/actuator-design-paper"
topic: "Task Based Motor Control Algorithm Design"
concepts:
  - "Co-Design Optimization"
  - "D-Axis Control"
  - "BLDC Actuators"
  - "Current Amplification"
source: Substack
author: Avik De
---

# Task-based motor control algorithm design

![](https://substackcdn.com/image/fetch/$s_!ambP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F487f3e6e-bc13-4773-b963-739da1e901d4_788x303.png)

*Paper in RAL 2019 about applying task-specifics to BLDC control*

> Originally published: [2019-01-23](https://www.avikde.me/p/actuator-design-paper)

**Topic:** [[topics/task-based-motor-control-algorithm-design|Task Based Motor Control Algorithm Design]]
**Concepts:** [[concepts/co-design-optimization|Co-Design Optimization]] · [[concepts/d-axis-control|D-Axis Control]] · [[concepts/bldc-actuators|BLDC Actuators]] · [[concepts/current-amplification|Current Amplification]]
**Citations:** [[citations/pmdcorp-com|pmdcorp.com]] · [[citations/speakerdeck-com|speakerdeck.com]]

---

In keeping with my broad interest in optimizing robot design, in this project1, I looked at co-design of the motor control algorithm for a BLDC actuator with the task at hand. Normally in [field-oriented control](<https://www.pmdcorp.com/resources/type/articles/get/field-oriented-control-foc-a-deep-dive-article>), a motor controller is purely programmed as a current amplifier — higher-level algorithms output a desired current, and the motor control algorithm attempts to ensure that the quadrature current tracks the desired current while minimizing the direct current.

However, looking at the task more broadly, there are situations in robotics when the task calls for high-speed motion, or urgent braking. In these types of instances, this paper shows that incorporating task-specific cues in the motor control algorithm can yield superior performance to treating it as a black-box current amplifier.

[![](https://substackcdn.com/image/fetch/$s_!ambP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F487f3e6e-bc13-4773-b963-739da1e901d4_788x303.png)](<https://substackcdn.com/image/fetch/$s_!ambP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F487f3e6e-bc13-4773-b963-739da1e901d4_788x303.png>)**Left:** “Braking task” tested in the paper; **middle:** actuator with customized motor control algorithm; **right:** simplified motor geometric model used for task-based motor sizing in the paper.

### Results

For the braking task specifically, we were able to show improved performance when incorporating d-axis control (i.e. deviating from standard field-oriented control, where the d-axis voltage is strictly used to minimized d-axis current):

[![](https://substackcdn.com/image/fetch/$s_!fo8Q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F738f5b54-9daa-4020-b672-192b69e747c3_671x509.png)](<https://substackcdn.com/image/fetch/$s_!fo8Q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F738f5b54-9daa-4020-b672-192b69e747c3_671x509.png>)Results of using d-axis control (moving away from 0 on the horizontal axis) showing improved performance in the braking task.

There are also results in the paper of utilizing these principles to affect the design of the motor itself.

Overall, the broad strategy here is to take advantage of full vertical integration and customization of various parts of the hardware stack. I haven’t seen any instance of any lab-grown or commercial robotics hardware do this yet, but I think it could be an interesting avenue to explore in resource- or power-constrained hardware.

[Link to slides from the talk](<https://speakerdeck.com/avikde/operating-at-force-power-and-thermal-limits-in-electrically-actuated-commercial-legged-robots>)

Thanks for reading min{power} by avikde! Subscribe for free to receive new posts.

Youtube recording of a workshop talk I gave including this topic:

## 

1

Link to paper: [Task-based control and design of a BLDC actuator for robotics](<https://scholar.google.com/citations?view_op=view_citation&hl=en&user=m-A4ZdEAAAAJ&sortby=pubdate&citation_for_view=m-A4ZdEAAAAJ:bKqednn6t2AC>)
