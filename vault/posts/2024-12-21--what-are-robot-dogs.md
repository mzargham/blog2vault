---
title: "What are robot dogs, and what are they good for?"
subtitle: "A brief what and why of quadrupedal robots, originally drafted for a magazine article"
date: 2024-12-21
slug: what-are-robot-dogs
canonical_url: "https://www.avikde.me/p/what-are-robot-dogs"
tags:
  - robotics
concepts:
  - "Rise"
source: Substack
author: Avik De
---

# What are robot dogs, and what are they good for?

*A brief what and why of quadrupedal robots, originally drafted for a magazine article*

> Originally published: [2024-12-21](https://www.avikde.me/p/what-are-robot-dogs)

**Topics:** [[topics/robotics|Robotics]]
**Concepts:** [[concepts/rise|Rise]]
**Citations:** [[citations/nature-com|nature.com]] · [[citations/tyndall-af-mil|tyndall.af.mil]] · [[citations/youtu-be|youtu.be]] · [[citations/overtdefense-com|overtdefense.com]] · [[citations/cincinnati-com|cincinnati.com]]

---

I was recently contacted by a journalist for a magazine article about quadrupedal robots (what they are, what they are good for, etc.). It was a good exercise in processing my own thoughts, and since only a small amount of them ended up making it into the publication, I’ll record them here.

> Robots tend to imitate naturally occurring, biological structures. What is it about a dog’s form that makes it ideal to roboticize?

The field of bio-inspired robotics is the result of close collaboration between biomechanists and roboticists. It is a synergistic discipline, where biologists study animals and distill their functioning principles into lessons that engineers can use to design robots. In the other direction, machines built with simple mechanisms and programmable behaviors provide testable hypotheses for the biologists to deepen their understanding of animals.

It’s important to note that useful robots are not usually created by mimicking animal form (biomimetics), but rather by taking inspiration from their working principles (bioinspiration). Engineers have access to different materials and power sources than those available to biological creatures, and animal bodies have evolved to serve many functions that are not relevant to a robot. For this reason, a four-legged robot may roughly resemble a dog’s form, and in particular move in a manner resembling a dog, but will not copy the intricate details of its biological structure.

Four-legged animals like cats or dogs usually walk on their toes (digitigrade), while humans and other two-legged animals walk on flat feet (plantigrade). This is related to the fact that the larger feet allow for a lot more control over balance than the toe-tips (imagine a human standing on one leg, compared to a cat or dog). In practical terms for engineers, this means that the legs of two-legged robots are a lot more complex, with many actuators needed for the hip, knee, and ankle in order to balance. In comparison, a four-legged robot can have much simpler leg designs, with no ankle or foot needed at all. In fact, typically, a four-legged robot has fewer motors than a two-legged robot, reducing cost and complexity, while having good agility and balance over difficult terrain.

> Can you walk me through how a robot dog works/functions?

The body of a four-legged robot has four simple legs that can position the toe at any point within reach. For the robot to stand in place, four of these toes are in contact with the ground, and the forces generated using the motors in the leg create a reaction force on the body, thereby supporting it. When the robot needs to move, some of these legs leave the ground and swing through the air to reposition the toes in the direction of movement, or simply to find a better foothold. While the algorithms used to calculate these forces or where to reposition the legs can get quite complex, the basic working principle is simple: If you recall the last time you had to scramble up some terrain on a difficult hike, the idea of using limbs to either push against the ground, or reposition them, will seem quite familiar. These same principles are applied by algorithms to select when and where to reposition which legs, so that the robot stays balanced as it moves over different types of terrain.

Unlike wheeled vehicles, legged robots can move over broken or discontinuous terrain by picking isolated footholds, allowing them to go into locations without roads or trails. Other than the legs, the body of the robot contains a power source (typically a battery), computing devices to run the aforementioned algorithms, and sensors needed to sense the environment around the robot.

> The Vision series includes some of the most successful quadrupeds to date. Can you elaborate on certain design features that make it superior to other models?

Despite the recent rise in popularity of legged robotics, we are still discovering newer and more impactful use-cases for this technology, and these applications inform which features robot manufacturers prioritize.

One important feature is energetic efficiency, which needs careful attention in all building blocks of a four-legged robot, ranging from its design to the algorithms used to control its motion. In the longer-term hopeful future of a proliferation of these robots in various use cases, this focus will allow a positive weighting of their utility against their energy consumption. Emerging technologies like artificial intelligence (AI) are currently having to [contend with this cost-benefit analysis](<https://www.nature.com/articles/d41586-024-03408-z>), and legged robots will be no different.

It is also important–because the technology is so new–to embrace developers and empower them to customize the robot to solve new problems. A wide range of peripheral connectivity options and a software developer kit can enable (for example), the development of a [hose-pointing behavior for firefighter support](<https://www.instagram.com/p/DCHxxlOPjga/>). Much like an app store amplifies the utility of a smartphone, customizability will increase the utility of legged robots in niche but impactful use cases.

> What are some of the trickier aspects when it comes to developing a robot dog? What challenges are developers in this space currently facing?

Locomotion in challenging terrain requires cutting-edge algorithms, spanning from traditional methods that leverage classical physics principles, to ones that use machine learning to learn from experience and data. In either case, more sophisticated strategies may result in increased functionality, but at the expense of more computational power and fragility to changes in the robot hardware, operating environment, or payload. Balancing the utility of an algorithm against its computational footprint and sensitivity is a difficult task for roboticists.

It is also challenging to increase the battery life of a legged robot. It needs to carry its power source, and so while installing a larger battery would increase battery life, doing so may introduce other issues such as reduced payload capacity. Improvements in battery energy density and microprocessor computational efficiency are innovations that are currently outside of the scope of our in-house research team, and the efficiency of electric motors for legged robots is limited by the fundamentals of electromagnetics. This leaves robot designers with difficult optimization problems in mechanical design and algorithm selection as some of the only tools available to increase their running time.

Lastly, legged robots are complex electromechanical machines, currently being designed and built by research-oriented organizations that only have limited manufacturing experience. Eventually, legged robots will be able to be mass-produced with the same reliability and cost-effectiveness that we have come to expect from automobiles or household appliances, but getting to that point requires scale that will only come with time and expanding applications for these robots.

> Future of robot dogs: As robotics and AI become more integrated into industry and even daily life, how do you see robot dogs being applied in the near future? Especially considering the wide variety of attachment possibilities.

Four-legged robots are very versatile platforms that exhibit good mobility, payload capacity, and range for a given size and weight. This means that they are able to carry sensors and payloads (attachments) for long missions, in built environments including stairs, or in rugged outdoor terrain. This makes them very suited for automating tasks such as [security](<https://www.tyndall.af.mil/News/Article-Display/Article/2550793/tyndall-brings-in-the-big-dogs/>) and equipment inspection, surveying, and [mapping](<https://youtu.be/vpVlX1z4sFs?si=J7DdRv9tut0Z1S82>). These jobs currently involve workers going into remote locations, hazardous environments, or performing repetitive tasks, and are ripe for automation. Automated inspection and security call for payloads such as high-resolution, thermal, electro-optical, or low-light cameras, acoustic imagers, and hazardous gas sensors.

These robots also provide a great deal of utility as the eyes and ears of first responders, going first into dangerous situations such as [disaster](<https://www.overtdefense.com/2024/01/19/japans-ground-self-defense-force-deploys-robot-dogs-to-aid-earthquake-relief-efforts/>) [response](<https://www.cincinnati.com/story/news/2024/11/10/daniel-carter-beard-bridge-fire-odot-uses-robodog-to-assess-damage/76126394007/>), and response to chemical, biological, radiological, nuclear, or explosive ordnance (CBRNE). For these applications, payloads such as multi-gas detectors, raman spectrometers, radiation, and explosive trace detectors are useful payloads.

> Why is this tech important?

As the focus grows on the hazardous and unsafe conditions faced by workers across the world, it will be important for us to come up with machines and tools to perform these dull, dirty, and dangerous tasks in their stead. Parallel to the rapidly increasing utility and footprint of informational automation with AI, there is a need for automation of physical work, such as carrying sensors and other payloads, accessing dangerous locations, and automating mundane physical tasks. Four-legged robots are a flexible and versatile platform that have the potential to be adapted to all of these use cases in a cost- and energy-efficient manner.
