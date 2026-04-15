---
title: "Minitaur bounding, pronking using vertical hopper compositions"
subtitle: "Simple controllers produce exciting quadrupedal behaviors - paper in IJRR 2018"
date: 2024-12-22
slug: vertical-hopper-compositions
canonical_url: "https://www.avikde.me/p/vertical-hopper-compositions"
tags:
  - research
concepts:
  - "Location"
  - "Averaging"
source: Substack
author: Avik De
---

# Minitaur bounding, pronking using vertical hopper compositions

![](https://substackcdn.com/image/youtube/w_728,c_limit/ijnOCQOpC7k)

*Simple controllers produce exciting quadrupedal behaviors - paper in IJRR 2018*

> Originally published: [2024-12-22](https://www.avikde.me/p/vertical-hopper-compositions)

**Topics:** [[topics/research|Research]]
**Concepts:** [[concepts/location|Location]] · [[concepts/averaging|Averaging]]
**Citations:** [[citations/mitpress-mit-edu|mitpress.mit.edu]] · [[citations/en-wikipedia-org|en.wikipedia.org]] · [[citations/sciencedirect-com|sciencedirect.com]]

---

Extending1 the methodology for [hopping behaviors on Jerboa](</jerboa-hopping-video>) to [Minitaur](</ghost-robotics-minitaur>) required understanding how to compose monopedal hopping primitives onto a quadrupedal robot. To do this, we built on the old idea of virtual bipeds, but in a way that would be compatible with the formal guarantees of the hybrid averaging framework that we had been publishing at about the same time:

Using simple bottom-up, decentralized, decoupled controllers, we were able to show a wide range of gaits working stably on Minitaur, with pretty good performance:

### Virtual bipeds

The way we used the idea of virtual bipeds here was to “project” the coordinates roughly along the gray arrows, and “pair” the legs projected together.

[![Virtual biped](https://substackcdn.com/image/fetch/$s_!PAro!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F379265d8-9c3f-4a86-b405-74481e944c38_596x472.png)](<https://substackcdn.com/image/fetch/$s_!PAro!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F379265d8-9c3f-4a86-b405-74481e944c38_596x472.png>)Virtual bipeds

After this projection, we are left with a kind of planar bipedal system to analyze with three degrees of freedom, as shown in the right column above.

### Vertical hopper compositions

Focusing on the bound/pronk projection, the types of limit cycles for these two gaits look like the flows roughly resembling the following picture:

[![Vertical hopping limit cycles pronk bound](https://substackcdn.com/image/fetch/$s_!rQPj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0bb5f961-cf99-4b08-97d6-524e1fb50b7e_486x648.png)](<https://substackcdn.com/image/fetch/$s_!rQPj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0bb5f961-cf99-4b08-97d6-524e1fb50b7e_486x648.png>)Bipedal “gaits” showing bounding and pronking

Looking more closely the picture above, the axes in the plot are the “phases” of the two legs, a concept we talked about in the accompanying [hybrid averaging](</hybrid-averaging>) paper. That identification now encourages us to think about our original quadruped as a pair of (vertical) hoppers “coupled” by a body.

The “coupling” is physically instantiated by the body itself, and its inertia properties have a significant effect on the type of coupling. The [center of percussion](<https://en.wikipedia.org/wiki/Center_of_percussion>) is a well-studied property of baseball bats, juggling clubs, etc. that relate impulses on one end of the object to the wrench on a different point along the object. We used this definition:

[![Center of percussion](https://substackcdn.com/image/fetch/$s_!U_a3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0367ebe6-d03a-412a-948f-b55d89a41f04_746x454.png)](<https://substackcdn.com/image/fetch/$s_!U_a3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0367ebe6-d03a-412a-948f-b55d89a41f04_746x454.png>)Center of percussion

Intuitively, the location of the center of percussion, which is in turn related to the mass distribution of the object, affects the type of coupling between the two hoppers.

### Pronking and bounding

We showed using simulation, and by physically altering the inertia characteristics of sagittal-plane Minitaur by adding an “inertia bar” to its back, that we could indeed get both bounding and pronking limit cycles by programming its front and rear ends as completely independent vertical hoppers:

This is a bit of an extreme interpretation of the style of decoupled control originally pioneered by [Raibert](<https://mitpress.mit.edu/9780262681193/legged-robots-that-balance/>) and also demonstrated on [Jerboa](</jerboa-hopping-video>), but it also has interesting implications on the possibility of [distributed control](<https://en.wikipedia.org/wiki/Distributed_control_system>) of legged robots. Another way to think about it is that we are formalizing [preflexes](<https://en.wikipedia.org/wiki/Preflexes>), which have historically played a pivotal role in the mechanical stabilization of animal and [robot](<https://www.sciencedirect.com/science/article/abs/pii/S1467803904000398>) locomotion.

Thanks for reading min{power} by avikde! Subscribe for free to receive new posts.

1

 _The[paper](<https://scholar.google.com/citations?view_op=view_citation&hl=en&user=m-A4ZdEAAAAJ&citation_for_view=m-A4ZdEAAAAJ:cWzG1nlazyYC>) corresponding to this article was published in 2018_
