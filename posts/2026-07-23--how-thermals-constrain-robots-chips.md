---
title: "How Thermals Constrain Robots, Chips, and Space Datacenters"
subtitle: "Two general principles to understand and defeat overheating"
date: 2026-07-23
slug: how-thermals-constrain-robots-chips
canonical_url: "https://www.avikde.me/p/how-thermals-constrain-robots-chips"
topic: "Uncategorized"
concepts:
  []
source: Substack
author: Avik De
---

# How Thermals Constrain Robots, Chips, and Space Datacenters

![](https://substackcdn.com/image/fetch/$s_!fQR_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0968e24-a970-4b4c-8d7a-627f4c7eb424_1316x622.png)

*Two general principles to understand and defeat overheating*

> Originally published: [2026-07-23](https://www.avikde.me/p/how-thermals-constrain-robots-chips)

**Citations:** [[citations/tomshardware-com|tomshardware.com]] · [[citations/powerctc-com|powerctc.com]] · [[citations/ieee-org|ieee.org]] · [[citations/en-wikipedia-org|en.wikipedia.org]] · [[citations/ntrs-nasa-gov|ntrs.nasa.gov]] · [[citations/eu-36kr-com|eu.36kr.com]] · [[citations/mdpi-com|mdpi.com]] · [[citations/humanoid-press|humanoid.press]] · [[citations/parkplacetechnologies-com|parkplacetechnologies.com]] · [[citations/semiwiki-com|semiwiki.com]] · [[citations/chipinsights-net|chipinsights.net]] · [[citations/mit-edu|mit.edu]]

---

In a prior article, I wrote about the principles behind [designing record-breaking running robots](<https://www.avikde.me/p/honors-humanoid-ran-the-fastest-half>). As I wrote then, one of the most helpful innovations over commercial humanoids appeared to be thermal:

> What should we conclude from Honor’s accomplishment? First, the capillary motor cooling solution, if mass manufacturable, is a genuine advance, and I suspect this running pace would not have been sustainable without it.

In this article, I wanted to back up my claim about its _necessity_.

It might sound boring, but many devices we see around us are ultimately performance-constrained by thermals. In computing, all energy used is converted to heat. In machines and in robotics, where robots do physical work, a fraction of the input energy is converted to physical work, and the remainder is converted to heat. Heat results in higher temperatures, which ultimately causes failures in materials, mechanisms, and electronics. So, to increase your device’s performance, you need to understand heat transfer.

The _TL;DR_ version of this article: using helpful analogies, I’ll describe how to arrive at two very simple principles to understand heat transfer: (a) establish the paths for heat flow, (b) study the bottlenecks in the shortest path before optimizing anywhere else. We will also see how to apply these principles to 3 very different applications: running robots, AI chips, and space datacenters.

Thanks for reading min{power}! Subscribe for free to receive new posts and support my work.

## Three methods of heat transfer → one coefficient

Heat transfer at first seems quite complicated. There are three primary mechanisms by which it can occur:

  * **Conduction** : Primarily in solids, molecules literally pass kinetic energy along to neighbors in direct physical contact

  * **Convection** : Fluids “carry” the heat by moving it along its flow

  * **Radiation** : Happens through electromagnetic waves, without any matter needing to move (or even be present)




These are distinctly different mechanisms, but there are a few very important similarities. For all of these, the energy transfered _Q_ is proportional to both the **temperature gradient** _ΔT_ and the **area** _A_ of contact / exposure. In equation form,

where _h_ , the heat transfer coefficient, is often nearly constant over a range of operating conditions.

**This is an amazing fact!** If you characterize or learn _h_ somehow, you can model the relationship between the heat an object produces and what its temperature will be.

The problem is that a value of _h_ will only be valid for a particular configuration of materials and environment. For example, if your device has a vertical exterior wall in still air, you can expect _h_ ≈ 4.2 W/m2K (**W** atts, **m** eters, and **K** elvins appear in those units). But what if the exterior wall is made up of an exterior metal shell over an insulating plastic layer? What if there are vibration dampening grommets? Screws? Electronics? Any real device will be constructed of many materials and interfaces. How do we apply the equation above?

## The circuit / flow analogy

Let’s think of the flow of heat as being represented by the flow of water through pipes. “ _h_ ” says something about the thickness of the pipe, and how much it _resists_ the flow.

At this juncture, if you’ve ever taken a circuits class, some bells may be ringing — flow of water through pipes is also the analogy typically used to explain the flow of electrons through circuits.

The analogy suggests a method of handling the complexity of multiple materials and interfaces — a circuit of resistors1 in series and parallel! The thermal resistance quantity _R_ has units of K/W. You start with _h_ and multiply it by the effective area through which the transfer occurs. Here’s a simple example combining conduction and convection from the inside of a solid cylinder to the air outside:2

[![](https://substackcdn.com/image/fetch/$s_!xFgG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F095f0241-50c0-4c87-8d6c-946837461e23_1226x334.png)](<https://substackcdn.com/image/fetch/$s_!xFgG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F095f0241-50c0-4c87-8d6c-946837461e23_1226x334.png>)

It is helpful to introduce an intermediate quantity called thermal conductivity _k_ with units of W/(m.K), and combine with a characteristic length. If you look at datasheets of [thermal paste](<https://www.tomshardware.com/best-picks/best-thermal-paste>) or [thermal pads](<https://powerctc.com/news-detail.php?id=5632>) for chips, they will be labeled with the _k_ value. You simply multiply that with the thickness of the pad or paste layer and take the reciprocal to get resistance in K/W. In the pipe flow analogy, a pipe of a certain diameter has a fixed _k_ value — the resistance is simply proportional to the length of the pipe segment.

These circuits can get very complicated, but finding the equivalent resistance is still a straightforward process.

[![](https://substackcdn.com/image/fetch/$s_!72iv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10f54038-1dc9-4e1d-b6c6-e1b54ba0a120_1390x867.png)](<https://substackcdn.com/image/fetch/$s_!72iv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10f54038-1dc9-4e1d-b6c6-e1b54ba0a120_1390x867.png>)A (very complicated) lumped-parameter thermal network (LPTN) for a motor ([source](<https://ieeexplore.ieee.org/document/9346016>))

There are three important takeaways to remember:

  1. You can use equivalent circuits to “build up” the value of _R_ (in K/W) for complicated arrangements of materials.

  2. Once you have _R_ in K/W, you can multiply it with the power generated as heat (in Watts) to get the temperature rise (in Kelvin or Celsius).

  3. The pipe flow analogy makes it clear that a narrow pipe, even when in series with a fat pipe, can be a bottleneck. In the simple series conduction-convection circuit above, if _R cond_ is high, there is very little that can be done with _R conv_ to improve the situation, since the equivalent is (_R cond \+ Rcond_)!




Let’s apply these takeaways to the running humanoid robot.

## Cooling a Robot Motor

The main heat generating element in a motor is the copper winding through which current flows in order to generate a magnetic field. This heat must travel from the winding, through the stator core, and through the housing, outward. In many research papers (e.g. [Urata 2008](<https://ieeexplore.ieee.org/document/4651110>)), this is lumped into a “mostly conduction” interior pathway from the windings to the housing, and a “mostly convection” exterior pathway from the housing to ambient:

[![](https://substackcdn.com/image/fetch/$s_!fQR_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0968e24-a970-4b4c-8d7a-627f4c7eb424_1316x622.png)](<https://substackcdn.com/image/fetch/$s_!fQR_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0968e24-a970-4b4c-8d7a-627f4c7eb424_1316x622.png>)

In most robots, thermal management paths are to do with the latter (housing outward). This can include air cooling (potentially a fan near the housing) or a [water cooling jacket](<https://ieeexplore.ieee.org/document/4651110>):

[![](https://substackcdn.com/image/fetch/$s_!8pjL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1790614-061f-4ca1-aa71-8f073770b4dd_669x410.png)](<https://substackcdn.com/image/fetch/$s_!8pjL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1790614-061f-4ca1-aa71-8f073770b4dd_669x410.png>)

With our principles from the previous section, let’s dig into the interior winding → housing pathway.

It’s unfortunately complicated. The copper itself needs electrically insulating enamel so that the windings don’t short, the coils go on separate stator teeth with gaps between them, and there is usually an interface between the stator iron and housing. The gaps between the teeth can be dry or [potted](<https://en.wikipedia.org/wiki/Potting_\(electronics\)>) with a thermally conductive but electrically insulating material.

Fortunately, there is a lot of research data on the **equivalent conductivity** _k eq _of this layered system.

Following [Sarma](<https://ieeexplore.ieee.org/document/11145781>), we can relate the thermal resistance to an equivalent conductivity _k_ and geometry of the motor

[![](https://substackcdn.com/image/fetch/$s_!wgxO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb0da0af-334c-4ce0-9773-28e24944b545_752x97.png)](<https://substackcdn.com/image/fetch/$s_!wgxO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb0da0af-334c-4ce0-9773-28e24944b545_752x97.png>)

In our [case study of the humanoid robot motor](<https://www.avikde.me/p/honors-humanoid-ran-the-fastest-half>), we used an ILM115x25 motor, for which the inner and outer diameters are 86mm and 115mm and axial length _L a _≈ 50mm (choosing slightly longer than the stack length).

For the conductivity _k_ , Sarma provides values for a spectrum of constructions, which result in the following range of thermal resistances:

  * Dry winding (no potting): _k eq_ = 0.1 W/m.K → _R cond_ ≈ **9 K/W**

  * “Good” humanoid-joint motor: _k eq_ = 0.85 → _R cond_ ≈ **1 K/W**

  * YASA axial flux: _k eq _= 1.8 → _R cond_ ≈ **0.5 K/W**

  * [NASA HEMM](<https://ntrs.nasa.gov/api/citations/20190002832/downloads/20190002832.pdf>) potted Litz wire: _k eq _= 3.5 → _R cond_ ≈ **0.26 K/W**




Of these, the most applicable value is the second one, but let’s say we are optimistic and can make a thermally “really good” motor, and get the resistance down to **0.7 K/W**.

Still, we have a problem!

As I showed in my prior article, the half-marathon running robot needs to dissipate 150 W continuously, and even the “really good” motor will increase its temperature by (at least) **105 C**!

What if we continue our “really good” thermal engineering and put a fan on the outside of the motor for really low convection resistance _R conv_? Unfortunately, as the equivalent resistance (series) is **never going to be smaller than** _R cond_, we cannot lower our motor temperature whatever exterior cooling we apply!

Is there any way out?

[Subscribe now](<https://www.avikde.me/subscribe?>)

## Honor’s solution: capillary liquid cooling

Let’s revisit [what Honor did](<https://eu.36kr.com/en/p/3775418378027520>):

> According to Honor, the liquid - cooling pipes penetrate deep into the motors like capillaries. The high - power liquid pump has a heat - exchange flow rate of more than 4 liters per minute. Each of the four drive motors in the lower limbs is equipped with an independent liquid - cooling circuit.

There is no public information on the detailed construction, but here is an image of a similar idea from a [research paper](<https://www.mdpi.com/1996-1073/16/19/7006>):

[![](https://substackcdn.com/image/fetch/$s_!N5Qg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde131e71-8e26-4db5-9c2e-a231d9a6deb6_1422x1058.png)](<https://substackcdn.com/image/fetch/$s_!N5Qg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde131e71-8e26-4db5-9c2e-a231d9a6deb6_1422x1058.png>)

The key here is the breakdown of the internal conduction path. 

  1. The capillaries use liquid (which has significantly higher convective heat transfer capability than a gas)

  2. The capillaries get much closer to the coils themselves

  3. The exterior convection can take place across a much larger radiator area (instead of being limited to the area of the motor housing)




Here’s a rough numerical analysis of how this works.

Assume Honor runs _N_ capillaries of 1 mm diameter through a motor. At [4 L/min](<https://humanoid.press/database/humanoid-press-database-honor-lightning/>) total flow and 4 independent circuits, each leg gets 1 L/min flow. So the

  * Liquid velocity in each capillary: v = _FlowRate_ / (_N_ _CrossSection_) ~= 2 m/s

  * Table 1.1 in AHTT lists a few similar scenarios, say _h cap_ ~ 3500 W/m2K conservatively

  * For 10 capillaries of 50 mm length, the total wetted area inside the stator is _A cap =_ _N π D L_ ≈ **0.0015 m 2**

  * So the thermal resistance is _R = 1 / (h cap Acap_) = **0.19 K/W**




This baseline is significantly improved from the conventional scenario above!

Let’s do a very brief exterior cooling _R conv _estimation following Table 1.1 from the Heat Transfer Textbook.

[![](https://substackcdn.com/image/fetch/$s_!WxWJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F921d1b86-4546-4909-b875-924f60f5ffa5_1099x483.png)](<https://substackcdn.com/image/fetch/$s_!WxWJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F921d1b86-4546-4909-b875-924f60f5ffa5_1099x483.png>)

For a good fan, we’d get 50 W/m2K, and let’s say the radiator is a 30cm square, i.e. _A radiator_ = 0.09 m2, and so _**R conv **_**= 0.22 K/W.**

In sum, with all this good engineering, we’re down to a total of **0.41 K/W**. On top of this, radiation will also help slightly, reducing this value further.

Now, with a 150 W generated in the knee motor, we’re looking at a much more reasonable 60 C temperature rise.

Thermals never seem like a _fundamental_ constraint of physics, like force or power limits, but they are just as real!

As noted in the numbered list above, the capillaries allowed us to (a) get closer to the heat source, and (b) decouple the convection area from the motor geometry itself.

Without (a), the heat would be bottlenecked inside the motor, and without (b), it would be bottlenecked getting discharged from the housing.

These two general principles are applicable much more broadly.

## Chips and Space Datacenters

Computer chips can consume hundreds of Watts, but unlike motors, they do no physical work. All of those Watts need to be dissipated as heat.

Fortunately, unlike a motor, the physical size of the chip is small (shorter thermal pathway) and there are fewer different types of materials and thermal interfaces inside the chip.

Conventional chip cooling has utilized a short interior thermal path: _R cond_ encompasses the path from the transistors to the [Integrated Heat Spreader (IHS)](<https://www.tomshardware.com/reviews/integrated-heat-spreader-ihs-definition,5747.html>), or [directly to the top of the die](<https://www.parkplacetechnologies.com/blog/direct-to-chip-cooling-how-it-works-effectiveness/>). The rest of the path (which we lumped into _R conv_) can involve heat pipes and a radiator, or a liquid cooling loop.

As with our motor example, as you can imagine, whatever you do with _R conv_, you are limited by how good _R cond_ can be. This is referred to as the “thermal wall” and there is ongoing R&D into [effectively integrating capillaries](<https://semiwiki.com/semiconductor-manufacturers/362017-breaking-the-thermal-wall-tsmc-demonstrates-direct-to-silicon-liquid-cooling-on-cowos/>) just like the motor:

> TSMC’s Direct-to-Silicon Liquid Cooling redefines this paradigm by embedding microfluidic channels directly into the silicon structure, bypassing TIMs for near-zero thermal impedance. At the heart of this technology is the Si-Integrated Micro Cooler, a silicon-based solution fusion-bonded to the chip’s backside.

* * *

There has been a lot written about putting [data centers in space](<https://spectrum.ieee.org/orbital-data-centers-heat>), but to understand the cooling challenge you just need to again apply the same two principles. Even if you do incredible thermal engineering inside the space datacenter (reducing _R cond_), you are stuck with the fact that the exterior cooling via _R conv_ is dismal because there nothing but vacuum around. Radiation is the only method of actually dispensing this heat, and becomes the bottleneck.

## Final thoughts

Because of the laws of thermodynamics, almost anything you do will generate heat. And if this heat cannot be dissipated, temperature-related failures kill your product.

Fortunately, a couple of relatively simple intuitive principles guide this effect, and understanding them will help you spend your time and effort judiciously. Honor figured this out for their record-breaking humanoid robot, and developed the correct intervention to sustain high-speed running.

The other remedy is to not generate the heat in the first place, by reducing power consumption and increasing efficiency. Good thermal performance shouldn’t be an excuse for bad design! For more reading on this topic, I’ll link to some articles about power optimization in chip design and robotics below.

_Thanks for reading! If you enjoyed this post, please like (❤️) and restack — it helps others find my writing. Subscribe to receive new posts._

[ Subscribe now](<https://www.avikde.me/subscribe?>)

[Share](<https://www.avikde.me/p/how-thermals-constrain-robots-chips?utm_source=substack&utm_medium=email&utm_content=share&action=share>)

[![](https://substackcdn.com/image/fetch/$s_!Z-fT!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74222e4c-9d04-46aa-82ba-7d82759b48b9_512x512.png)Chip InsightsThe Search for the Perfect MicroarchitectureTinyXPU is back…Read more19 days ago · 15 likes · Bharath Suresh and Avik De](<https://chipinsights.net/p/the-search-for-the-perfect-microarchitecture?utm_source=substack&utm_campaign=post_embed&utm_medium=web&embedding_publication_id=7287367>)

1

It goes deeper — capacitor charging can also help represent the transient change in temperature over time. In this article we’re sticking to steady-state effects, i.e. the capacitors are fully charged and can effectively be removed.

2

The source of this image, and much of the introductory content is the free [Heat Transfer Textbook](<https://ahtt.mit.edu/>) which I would highly recommend.
