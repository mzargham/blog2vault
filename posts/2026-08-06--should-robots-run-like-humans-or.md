---
title: "Should Robots Run Like Humans or Ostriches?"
subtitle: "Why different animals run differently, and what to take away for bio-inspired robotics"
date: 2026-08-06
slug: should-robots-run-like-humans-or
canonical_url: "https://www.avikde.me/p/should-robots-run-like-humans-or"
topic: "Uncategorized"
concepts:
  []
source: Substack
author: Avik De
---

# Should Robots Run Like Humans or Ostriches?

![](https://substackcdn.com/image/fetch/$s_!VuhR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f152c92-416d-41a1-b633-f3ca69c6f9bc_899x405.png)

*Why different animals run differently, and what to take away for bio-inspired robotics*

> Originally published: [2026-08-06](https://www.avikde.me/p/should-robots-run-like-humans-or)

**Citations:** [[citations/en-wikipedia-org|en.wikipedia.org]] · [[citations/science-org|science.org]] · [[citations/robot-daycare-com|robot.daycare.com]] · [[citations/youtube-com|youtube.com]]

---

Ostriches and humans are both capable terrestrial runners, and they both weigh about ~100kg in rough order of magnitude. However, they look quite different when they run. Take a look at these snapshots of a human running compared to an ostrich:

[![](https://substackcdn.com/image/fetch/$s_!VuhR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f152c92-416d-41a1-b633-f3ca69c6f9bc_899x405.png)](<https://substackcdn.com/image/fetch/$s_!VuhR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f152c92-416d-41a1-b633-f3ca69c6f9bc_899x405.png>)Panels sourced from [Muybridge](<https://en.wikipedia.org/wiki/Eadweard_Muybridge>)

My annotated lines show roughly where both legs are in the air (“aerial phase”). Why does a human have a much more prolonged aerial phase compared to an ostrich? What is different about these animals that could cause such a large difference in their preferred gait?

What does this tell us about how a robot should be designed and controlled to run?

Thanks for reading min{power}! Subscribe for free to receive new posts and support my work.

## Why animals run how they run

Animals typically run to optimize energetic efficiency. When being hunted by a predator (or as the predator), the more efficient runner can keep running for longer, and evolutionary pressure will select for that optimization.

But what optimizes energetic efficiency?

In a [previous article on a half-marathon-running robot](<https://www.avikde.me/p/honors-humanoid-ran-the-fastest-half>), I covered the basics of a very simplified model of running:

Given a stride period _T s_ (during which a leg goes through its stance and swing phases), and ground contact period _t c_, the “duty factor” _β=t c_/_T s _captures the difference between the ostrich (_β_ close to 0.5) and human (lower _β_) running.

Lower _β_ means that in the **stance period** , lasting _t c _seconds, the leg has to produce more vertical force, as shown in the following representative depiction (adapted from Biewener’s _Animal Locomotion_ book):

[![](https://substackcdn.com/image/fetch/$s_!b781!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c7aba77-20bf-4cb6-8225-066ddf75fdeb_1074x462.png)](<https://substackcdn.com/image/fetch/$s_!b781!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c7aba77-20bf-4cb6-8225-066ddf75fdeb_1074x462.png>)

Shortening _β_ increases how hard the muscles have to work, and increases the peak loading seen by the structural components.

So, _stance energetics drive toward high β._

In the **swing period** , lasting (_T s _\- _t c_) seconds, the leg needs to swing forward for the next foothold.

The hip muscles need to accelerate the inertia of the leg forward over this period. Remembering Newton’s second law, required force from the muscles scales with the inertia as well as acceleration. The higher _β_ is _,_ the shorter the swing period, and the higher the required acceleration.

So, _swing energetics drive toward low β._

* * *

Now, we have enough information to intuit why ostriches and humans run so differently. Ostriches have very skinny and light legs. Most of the leg is tucked in close to the body, and the distal foot is very long and almost entirely made of bone and tendon. All this results in **low leg inertia** compared the human, who has mass distributed along the upper and lower legs and a smaller foot.

So for the human, leg swing is energetically more expensive compared to the ostrich and it leans more toward lowering _β._ For the ostrich, leg swing isn’t so bad, and it moves _β_ up to reduce the impact of stance energetic expense. This explains the smaller aerial phases chosen by the ostrich, and the longer ones chosen by the human.

[Subscribe now](<https://www.avikde.me/subscribe?>)

## What about robots?

Many of the same principles apply to robots. Motors consume energy to produce force, and so you’d want to prolong stance as much as possible. Robot legs also have inertia, and you’d want to prolong swing as much as possible to reduce swing cost.

However, there is one factor that robot technology can leverage that can adjust the cost of force production: _**gearing**_. Let me explain.

* * *

Parts of this article were inspired by this excellent [recent review paper](<https://www.science.org/doi/10.1126/scirobotics.adi9754>) on how robots seem to have better available technology that animals, but still cannot perform1 as well:

[![](https://substackcdn.com/image/fetch/$s_!BWvA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F35c001d9-43a8-4b19-82a0-db8a75f4cbb5_1494x421.png)](<https://substackcdn.com/image/fetch/$s_!BWvA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F35c001d9-43a8-4b19-82a0-db8a75f4cbb5_1494x421.png>)

Specifically, when normalized for weight, while motors have similar ability to produce force, they can produce way more power than muscles.

[![](https://substackcdn.com/image/fetch/$s_!zqxl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd70e05d7-63c8-4dc3-900e-2768c19165bd_1203x224.png)](<https://substackcdn.com/image/fetch/$s_!zqxl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd70e05d7-63c8-4dc3-900e-2768c19165bd_1203x224.png>)

Gearing allows robots to change how much force a joint produces without (ideally) affecting its power output.

How does that change the stance / swing balance?

At first, it isn’t obvious. Adding gearing increases the “reflected inertia” of the motor when it is swinging the leg forward. This makes it require more effort to swing the leg. On the other hand, it reduces how much torque the motor needs to produce in stance.

How do we analyze these competing effects? It [turns out that](<https://www.avikde.me/p/honors-humanoid-ran-the-fastest-half>) based on the physics of motor construction, the torque produced by a motor, its inertia, and the amount of energy it consumes are related. This relation is also independent of gearing, and predictably [consistent across motors with orders of magnitude different size](<https://robot-daycare.com/posts/actuation_series_1/>). This allows us to reduce the entire (ideal) motor + gearbox robot drivetrain to a single independent parameter: the reflected motor inertia.

* * *

Now, we can get back to how a robot should pick _β_ — human- or ostrich-like?

Just like the animal, the robot wants _t c_ as long as possible (till the stance leg begins to have trouble reaching). Therefore, the total stride time _T s_ (including the swing period) is what is left to pick. I’ve plotted the average running power against the drivetrain inertia parameter and the stride time below:

[![](https://substackcdn.com/image/fetch/$s_!9pqI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a7428fd-bd9c-4d12-bfb2-95fe0ef5319d_890x778.png)](<https://substackcdn.com/image/fetch/$s_!9pqI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a7428fd-bd9c-4d12-bfb2-95fe0ef5319d_890x778.png>)

The result is very intuitive!

  * If the drivetrain has low inertia (like an ostrich leg), you should have a more grounded running gait with high _β_

  * If the drivetrain has high inertia (like a human leg), you should have a more bouncy gait




Crucially, _**robot gearing technology allows this to be pushed rightward arbitrarily**_. If you only care about energetics, a high-inertia (heavily geared) motor and a very bouncy gait would be more efficient.

To help visualize, this may look something like the “bounding” drill that track runners do ([source](<https://www.youtube.com/watch?v=b3124L0KK3Q>)):

Then why _don’t_ people design robots to run like this?

Firstly, the heavily-geared high-inertia drivetrain is more failure-prone at impacts (like when landing on the ground on each step). Series-elastic actuators (where the impact is absorbed by a spring) mitigate this particular drawback.

Secondly and more importantly, the robot needs to have ground contact to exert control. Long strides with slow cadence mean very low control bandwidth, and this kind of running is very difficult to control. If agility or maneuverability are needed to avoid obstacles or change direction, this kind of running is much more likely to cause a fall and failure.

These factors ultimately rein in the swing time for running robots. Nonetheless, the figure above clearly shows the coupled dependence between design (on the horizontal axis) and gait (on the vertical axis). Understanding that coupling helps answer the question of how a robot should run.

## Closing thoughts and further reading

The process we followed in this article was to try to understand the _principles_ that guide animals to run in a certain way. We then used these principles to take away lessons for robot design and control. This is process is called _bio-inspiration_.

What sometimes happens in robots (and what we shouldn’t do) is _biomimicry_. A contextual example of that would be copying the ostrich gait or copying the human gait directly. This article is a good example of where that can lead us astray.

_Thanks for reading! If you enjoyed this post, please like (❤️) and restack — it helps others find my writing. Subscribe to receive new posts._

[ Subscribe now](<https://www.avikde.me/subscribe?>)

[Share](<https://www.avikde.me/p/should-robots-run-like-humans-or?utm_source=substack&utm_medium=email&utm_content=share&action=share>)

If you enjoyed the coupling between design and control in this article, I’d recommend this one next:

1

The paper was submitted before [a robot beat the human half-marathon record](<https://www.avikde.me/p/honors-humanoid-ran-the-fastest-half>).
