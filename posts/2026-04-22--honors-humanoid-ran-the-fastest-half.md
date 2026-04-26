---
title: "Honor's humanoid ran the fastest half-marathon: how did they do it?"
subtitle: "Engineering isn't magic, it's a matter of tradeoffs"
date: 2026-04-22
slug: honors-humanoid-ran-the-fastest-half
canonical_url: "https://www.avikde.me/p/honors-humanoid-ran-the-fastest-half"
topic: "Humanoid Robot Marathon Performance"
concepts:
  - "Robotic Athletics"
  - "Human-Machine Performance Comparison"
  - "3D Locomotion"
  - "Biomimetic Control"
source: Substack
author: Avik De
---

# Honor's humanoid ran the fastest half-marathon: how did they do it?

![](https://substackcdn.com/image/fetch/$s_!S69N!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0d76f0f-f7a7-4a83-bf75-89e56c57428b_860x573.png)

*Engineering isn't magic, it's a matter of tradeoffs*

> Originally published: [2026-04-22](https://www.avikde.me/p/honors-humanoid-ran-the-fastest-half)

**Topic:** [[topics/humanoid-robot-marathon-performance|Humanoid Robot Marathon Performance]]
**Concepts:** [[concepts/robotic-athletics|Robotic Athletics]] · [[concepts/human-machine-performance-comparison|Human-Machine Performance Comparison]] · [[concepts/3d-locomotion|3D Locomotion]] · [[concepts/biomimetic-control|Biomimetic Control]]
**Citations:** [[citations/cnn-com|cnn.com]] · [[citations/en-wikipedia-org|en.wikipedia.org]] · [[citations/upenn-edu|upenn.edu]] · [[citations/robot-daycare-com|robot.daycare.com]] · [[citations/eu-36kr-com|eu.36kr.com]] · [[citations/apptronik-com|apptronik.com]] · [[citations/forbes-com|forbes.com]] · [[citations/gist-github-com|gist.github.com]]

---

Robotics headlines over the past week have been dominated by the news that the [Honor Lightning humanoid robot has beaten the human half marathon world record](<https://www.cnn.com/2026/04/19/china/china-robot-half-marathon-intl-hnk>) for the first time. It’s important to remember that machines and humans have very different capabilities and constraints, so why should we ever have expected the half marathon time for a robot and human to be related? Down the line, I don’t expect this particular comparison of human to machine to be very relevant. Nevertheless, it’s still an important milestone for engineering, just like [Deep Blue’s 1997 defeat of Garry Kasparov in chess](<https://en.wikipedia.org/wiki/Deep_Blue_versus_Garry_Kasparov>). From a human standpoint, I hope we can resist comparing the accomplishments of machines to the well-earned and deserved achievements of humans… maybe the chess model is a reasonable one here. Also as in the chess case, where Deep Blue couldn’t physically move the pieces, the Honor robot’s capabilities are much more narrow than a human running elbow-to-elbow with other runners, effortlessly navigating the course without GPS, etc. Comparing the robot runner to a human runner is just an apples to oranges comparison.

What _is_ a good comparison is this performance to last year’s, when the best robot time was over 160 minutes, or more than 3x this year’s time. That’s a remarkable improvement in one year. My doctoral thesis involved [building and controlling hopping and running robots](<https://www.avikde.me/p/phd-defense>), and [since then I’ve tried to design and build efficient commercial legged robots](<https://www.avikde.me/p/ghost-robotics-minitaur>), giving me a decent idea of the constraints involved. So, in this article I wanted to try and examine — how did they do it? Is there some magical technology or technique that unlocked this performance? How did they beat the significantly better-known Unitree (who reportedly had to supply an [ice pack backpack](<https://x.com/TheHumanoidHub/status/2045702643449037287>) to try and complete the race without overheating)? Could a western robot have won?

Thanks for reading min{power}! Subscribe for free to receive new posts and support my work.

_This publication and this post contain the author’s personal thoughts and opinions only, and do not reflect the views of any companies or institutions._

## The basic physics of hopping and running

Hopping, very simply, consists of alternating phases of a leg pushing against the ground (“stance phase”) and the body flying through the air (“aerial phase”).

In aerial phase, the body simply free-falls (constant acceleration due to gravity). You can think of this as losing vertical momentum. In stance phase, the job of the leg is to push against the ground to reverse this vertical momentum. The job of the “knee” actuator is primarily to generate this force in stance phase.

The other basic leg function is repositioning for the next foothold. In bipedal running, while one leg is pushing against the ground, the other leg is swinging to reposition for the next step. The job of the “hip” actuator is primarily to swing the leg forward.

Bipedal running is simply these two functions alternating in the two legs — while the left leg pushes against the ground, the right leg swings forward, and vice versa. Of course, this is an oversimplification in many ways, but it still captures the main effects that contribute to running energetics. Namely, it becomes clear that:

  * the knee actuator must produce enough torque to reverse the entire robot momentum in the stance duration _T s_

  * the hip actuator must product enough power to accelerate the leg forward in the swing duration _T sw_




The way a robot runs faster is that it increases its stride length and/or shortens the stance duration.

[![](https://substackcdn.com/image/fetch/$s_!RCSB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47bb499d-9875-46ab-bb45-0d4e0f7c8955_630x354.png)](<https://substackcdn.com/image/fetch/$s_!RCSB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47bb499d-9875-46ab-bb45-0d4e0f7c8955_630x354.png>)A depiction of a single-leg hopper’s stance phase showing the reversal of vertical momentum and the maintenance of horizontal momentum, as well as the stride length and the stance duration. Source: “Legged Robots That Balance”.

Shortening the stance duration requires a higher amount of knee torque to be needed to accomplish the same momentum reversal. Swinging the leg faster, and covering a longer stride length requires more torque and power from the hip actuator.

And just like that, with very basic physics, we’ve recovered the dependence of running speed on the torque and power produced by the actuators.

## The basic physics of motors

Electric motors dissipate energy in an exact relation to the amount of torque they produce, and these quantities are related by an appropriately-named constant termed the _motor constant_ , _K m_. If _τ_ is the torque produced by the motor and _Q_ is the heat it produces,

In the “New Motor Models” section in [my thesis (2017)](<https://repository.upenn.edu/entities/publication/10b266fd-41d2-49b6-ac90-0ee614bca00a>) I described how a _K m_ scaling relation can be approximated from rough first-principles geometry arguments. In particular, for a fixed length scale, _K m_ scales with the square root of motor mass √ _m_. In a [recent post](<https://robot-daycare.com/posts/actuation_series_1/>), longtime blogger and roboticist Ben Katz generalizes and gives this coefficient a name , the “figure of merit (FoM),” which we can use here:

The _r_ above is the motor diameter. To estimate motor mass _m_ , I decided to relate it to the motor diameter and (unknown) length. With these, and assuming a high but reasonable FoM of 15, we can extrapolate the likely _K m._

To estimate the rotor inertia, we can relate it to the motor mass and inertia as _j ~ mr 2_ as Ben Katz also does.

Adding a geartrain (gear ratio _G_) after the motor amplifies its torque and reduces its speed by _G_. So, it helps with torque production, but it has a very deleterious effect in legged systems when accelerating. Since the rotor of the motor itself has to spin faster, the rotor inertia _j_ in the output frame appears scaled to _G 2j_, which can quickly become very large. Thus, a small motor with large gearing becomes very sluggish at accelerating its output, even if it can statically produce a large torque. This is obviously bad for the “swing phase” described above.

## The Honor Lightning’s technology

There isn’t a technical report on this robot as far as I know, but some online articles list a few specifications. I referred to [this substack article](<https://chinaresearchcollective.substack.com/p/honors-autonomous-humanoid-robot>) for this post. A couple of notes:

  * This article and a few others say that the robot has 55 joints, but that is definitely a mistake. Potentially with hands (that were not equipped on these half-marathon versions) it could have 55 joints, but as deployed, they probably had closer to half as many joints.

  * The page also lists “Leaderdrive” as a harmonic reducer technology partner implying that strain wave gearing was used. However, based on the analysis below, a lower reduction-ratio planetary or another type of gearing is more appropriate, especially for this kind of efficiency-critical application.




### Actuation: motor, gearing, gait

These three factors are all interrelated and have an effect on how much energy is required and how much heat is produced. To see how, let’s start with the motor.

Typically, the motor _K m_ can be found in the datasheet, but in this case there’s no public reporting on the motor specs.

[![](https://substackcdn.com/image/fetch/$s_!S69N!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0d76f0f-f7a7-4a83-bf75-89e56c57428b_860x573.png)](<https://substackcdn.com/image/fetch/$s_!S69N!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0d76f0f-f7a7-4a83-bf75-89e56c57428b_860x573.png>)The Honor Lightning robot. Source: CNN.

However, we can see the size of the fairly large hip/knee motors attached to the upper leg (my rough estimation is that the outer diameter is somewhere between 110-150mm from the image above). We can look at a couple of potential options: first, a reasonable 115mm diameter catalog motor, which I chose from TQ’s frameless motor catalog for similar reasons to Ben Katz’s blog post — they are well-documented and have a large selection. Second, we can use the scaling principles to make some reasonably good approximations of _K m_ for a hypothetical larger motor. I extrapolated to a 150x25 sized motor to obtain a _K m_ of 1.52 Nm/sqrt(W), and a mass of almost 2 kg.

Since we don’t know the gear ratio, we can use our simple physics model (script linked in references below) to estimate the power consumption for running for the “small” and “big” motors above as a function of _G_ :

[![](https://substackcdn.com/image/fetch/$s_!DT76!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f426974-4bd6-496a-9abb-5f2bf4720cf4_682x564.png)](<https://substackcdn.com/image/fetch/$s_!DT76!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f426974-4bd6-496a-9abb-5f2bf4720cf4_682x564.png>)

Note that:

  * A high gear ratio is nice to minimize the power in the knee actuator (since its job of supporting the robot weight is made easier with mechanical advantage), but a high gear ratio also makes the leg swing energetically difficult.1 There’s usually a middle-ground optimum.

  * The larger motor (150x25) prefers a smaller gear ratio (~23:1), and the smaller motor (115x25) prefers a higher gear ratio (~40:1).2 These are shown with the dashed gray lines.

  * Both of these options seem to be able to accomplish the basic push-ground and leg-swing functions, with modest robot power consumption of 400-500 W.




So, in sum, the **motor is not magical technology** and in fact, a range of existing or projected options would work, _when appropriately sized for this task._**** I’ll get back to this last bit and the green lines in the plot later.

The dissipated knee power (which is typically the main thermal limiting factor) is ~150W for both solutions. This is almost an unavoidable consequence — due to the predictable scaling of motor _K m_, running at human speeds with a humanoid-sized robot will inevitably generate this amount of heat!

This, finally, is where we would see a potentially large difference between the two motors. Motor cooling is affected by the surface area over which heat removal can occur, and the larger motor has 70% more surface area. Even so, over a prolonged period, 150W is a large amount of power to dissipate from a single motor, and this is where one of the stated innovations in this robot design appear to be coming to bear ([source](<https://eu.36kr.com/en/p/3775418378027520>)):

> According to Honor, the liquid - cooling pipes penetrate deep into the motors like capillaries. The high - power liquid pump has a heat - exchange flow rate of more than 4 liters per minute. Each of the four drive motors in the lower limbs is equipped with an independent liquid - cooling circuit.

Liquid cooling is not new, but it’s definitely not what I would call a commodity. It has shown up in research periodically, and on the commercial side [Apptronik tried it for a few of their prototypes](<https://apptronik.com/news-collection/apptronik-readies-its-humanoid-robot-for-a-summer-unveil>) but (to my knowledge) does not use it on their main Apollo platform. While it definitely is not magical technology, it has been niche so far. As described above, it is absolutely essential (and so far quite challenging) to be able to dissipate ~150W from a motor for running at these speeds. From that respect, the **liquid cooling tech is a key enabler** of this type of performance.

Thanks for reading min{power}! Subscribe for free to receive new posts and support my work.

**Caveat:** The script I used to generate the plots above makes a lot of simplifying approximations. It doesn’t capture the energy dissipated in other motors (arms, ankles, abduction, etc.). The basic physics principles don’t lie about the periodic center-of-mass behavior, but this doesn’t model other oscillations in the orientation as the body sways etc., or losses like friction or air resistance. The inertia of the leg is left out of the swing inertia calculation, since there is no way to approximate it properly with the information available. Published materials emphasize a lightweight leg construction, which indicates that the rotor reflected inertia will likely dominate it (and so the script’s approximation is likely good). There are more accurate ways to estimate the swing energetics incorporating the leg kinematics and swing trajectory, but I wanted to not increase the complexity of this analysis and chose to err on the side of simplicity. Still, I think the main estimates and talking points (motor / gearing selection for the knee motor, and power dissipated in it) can be trusted.

### AI and autonomy

There’s nothing to write home about here. The gait controller could have used either a reinforcement learning (RL) controller, which is easy to train for flat ground, or a model-based controller. The autonomous navigation system used a provided GNSS system and just had to follow the route waypoints. This is all very well-understood technology.

### Battery

Let’s assume that the battery was chosen to last 1.5 hrs (the robot finished in < 1 hr). For 600 W consumption (based on the figures above with some buffer), the battery would have had to have 900 Wh capacity, and at 300 Wh/kg energy density, the pack would have weighed 3 kg. This is well within reason for a 45 kg robot. Additionally, a 1.5 hour discharge time indicates a 1/1.5 or 0.67C discharge, which is well within the ratings of most existing batteries.

The Unitree H1 reportedly needed “[pit stops](<https://www.instagram.com/p/DXZV1x9DEAp/>)” and battery cooling ice, indicating that it was consuming much higher power. We’ll talk about that more next.

## Engineering always involves tradeoffs

Engineering is always characterized by tradeoffs — that’s what makes it challenging but also fun. Especially today with ever-stronger AI language models, the very human skill of judgment and knowing how to made tradeoffs is much more important than the rote work of completing a design to spec.

Even with the very simple model above, it was not that complex to roughly design a drivetrain that is theoretically capable of this feat. Then why did the competitors in the race, including more [established and widely-shipped humanoids](<https://www.forbes.com/sites/johnkoetsier/2026/01/09/top-10-humanoid-robot-companies-by-shipments-revealed/>) such as from Unitree or Agibot, not compete as well?

We can use the simple model to generate an equivalent energetics plot for walking at 1.5 m/s, a much more modest but potentially more common activity for a commercial humanoid robot:

[![](https://substackcdn.com/image/fetch/$s_!5Gxy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fae713be7-bffb-4af2-871c-0433bdaaf6da_670x558.png)](<https://substackcdn.com/image/fetch/$s_!5Gxy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fae713be7-bffb-4af2-871c-0433bdaaf6da_670x558.png>)

The gray lines are as before — gear ratios optimized for half-marathon running. The green lines are where the power is minimized for walking, and they are significantly different!

Let’s say you design your robot to excel at the normal walking task and chose the green gear ratios. The knee motor power to run a half marathon with that green design consumes > 300 W, more than 2x what we had with the running-optimized gray designs. It wouldn’t be so surprising to need ice packs!

Conversely, the running-optimized gray design, when used for the walking task, wastes significantly more motor power than the green designs (as seen from where they intersect the blue curves). We couldn’t model this effect with the information available, but using larger motors sized for running also increases the weight of the robot and constantly wastes power when it isn’t running at full speed. You can visually see the difference in motor sizes between the Unitree H1 and Honor Lightning:

[![](https://substackcdn.com/image/fetch/$s_!kC_0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe087350a-1321-41e6-b2e6-ac50405051e9_2012x1776.png)](<https://substackcdn.com/image/fetch/$s_!kC_0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe087350a-1321-41e6-b2e6-ac50405051e9_2012x1776.png>)

The larger motors will have all sorts of practical (if not fundamental) consequences like bumping into objects while operating in homes or factories.

## Closing thoughts

What should we conclude from Honor’s accomplishment? First, the capillary motor cooling solution, if mass manufacturable, is a genuine advance, and I suspect this running pace would not have been sustainable without it. Second, even if there wasn’t any “magic” needed, this was a really impressive engineering effort and result. For better or worse, it deserves to be a landmark tantamount to Deep Blue v. Kasparov.

Having said that, I don’t believe this says anything at all about human half-marathon performances. It doesn’t even imply that a humanoid robot could join a race among a sea of people without GPS and resiliently finish the race. I wish those comparisons would be left out of the press coverage.

Another thing I found interesting is that the Lightning robot was reportedly developed in about a year, between MWC in March 2025 and the April 2026 race. That is incredibly fast. However, what is even more stunning is that the R&D team [reportedly had 2,600 people](<https://chinaresearchcollective.substack.com/p/honors-autonomous-humanoid-robot>). Comparing to a few US humanoid robot companies, to my knowledge, that eclipses the headcounts of Boston Dynamics, Figure, Agility, and Apptronik combined (I am not sure of Tesla’s Optimus-specific headcount). On top of that, you have to account for the partner and manufacturing ecosystem that was brought to bear, as reported by the same linked article.

Is all this worth it? It probably isn’t for most of these companies who need to spend their resources developing applications customers need and will pay for, but the cooling and weight-reduction advances may well be useful for more practical purposes like carrying heavy payloads down the line.

_If you enjoyed this post, please like (❤️) and restack — it helps others find my writing. Subscribe to receive new posts. All of this is greatly appreciated._

[ Subscribe now](<https://www.avikde.me/subscribe?>)

## References

  * [Script used for power estimates](<https://gist.github.com/avikde/496d108195a040763fd9b610f870d071>) (Github gist)

  * [Spreadsheet with motor parameters and estimates](<https://docs.google.com/spreadsheets/d/1spBdXsc9IK0wgs-ISgCVRF1hi4WsSuF2xuNKQCzFoPk/edit?gid=0#gid=0>)




1

This simplification makes it seem like one could just have a heavily geared knee motor and a lightly geared hip motor then, but this breaks down when you actually consider the full leg kinematics. Many of the leg joints participate in force production and swing, and one isn’t isolated to the knee motor like our cartoon might suggest. Additionally, a photo of the Honor robot really suggests that the hip and knee motors are similar if not identical. For the level of detail (and guesswork) of this article, we must assume that they are the same.

2

The larger motor will also make the whole robot heavier, but we don’t have sufficient information to predict how exactly so we have to ignore this effect
