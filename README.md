# gb_torch
A gameboy emulator attempt all in ASCII, generated mostly in one night by GPT4

ChatGPT journey dutifully documented here:
https://chatgpt.com/share/e5aa93c1-1308-4940-90fc-92ff25399b3c

Still WIP, needing debugging to get it rendering an arbitrary .gb file (aiming for PokemonRed, for a useful GPU-sped-up gym for AI agent testing from other sideprojects).  Gut says about 50% done toward a "working" version that at least pretty prints ROMs and does a few things before finding an edge case crash bug.  (8 more hours?)

I'm impressed by GPT4's ability to generate this, but there's certainly a bit of programmer effort (and only a tiny bit of personal intelligence) involved - unfortunately!  The true masterpiece will be when we can create complex code like this fuelled with nothing but lazy childlike wonder, but oh well.  Soon.

Closing analyses: 

===== 

```
Alright it's pretty late and about quitting time on this experiment!  Havent gotten it playing Pokemon yet, but it feels close - and at least doesn't throw out missing opcodes errors.  We did manage to do the following though:

- Made a 350 line gb_torch emulator that at least partially is built around emulating a gameboy rom on a gpu.  Probably someone does this better out there, but hey - this was an experiment in GPT4 coding as much as anything.  We manage to load, display registers, have specific memory controllers, and display an ASCII display (wanted ASCII since any feedback of images here would make this chat unshareable, which was the whole point.  Also it would be super cool to get an ASCII gameboy emulator)

-  Made another 150 lines of memory bank controller placeholder code that nonetheless does the trick for now probably(?)

- And made 720 lines of opcode for the emulator functions, which I'd actually bet are accurate more often than not.   But obviously this all needs testing.

Not bad for 8 hours of low effort prompting, but not great.  Lotta ways this coulda been done better - particularly in the opcode stuff where it's clear I could be prompting more efficiently.  I don't think my prompts were especially complex and informed throughout here (I tried to keep it stupid and lazy, both because this should be fun and low effort, and it's a test of GPT4 capabilities)  but it still probably shows that a programmer was helping here.  Nonetheless, this is still a project I would never even attempt under normal circumstances, lettalone expect to get this far in a night., so I'm at least quite impressed with the capabilities here - and see plenty of additional potential to further automate the meta-prompting for this kind of thing.

I do wish I had a working emulator at the end of this, but looking like that might require a level of genuine understanding and research (or at least rigorous auto-generated testing through that Moon-whatsit gameboy emulator test repo).  Considering that understanding and reading those complexities seems like *far* more mental work than just asking a question and copy-pasting, I was reluctant to take such avenues, but would in a followup session if I come around to trying to get this actually working.   So eh - call it halfway done.  The hard part of debugging and testing lays ahead, but GPT4 got us this close at least!  And that test generation is entirely in its wheelhouse too I reckon, but the real trick is file size is starting to creep up, and splitting files too much start to create consistency errors without a bit of clever overhead management.  Basically - we're nearing the point where GPT4 code assist should be wrapped in a smarter system (like Devon or the like - though I haven't messed with those much personally just yet, and would prefer to craft my own).  This also probably would have benefitted strongly from an informed, smart general architecture from the start (especially in e.g. the opcodes, which you can see in the prompt story).  I entirely went the lazy way and just asked chatgpt for those all, and it shows.  But again - that was kind of the point of this experiment too.

For now, mixed bag conclusion - I'm sure someone scouring this code would claim it's more work to debug than to have just built from scratch by a proper programmer.  Wish I had a working emulator at the end of this to just immediately refute that lol - but oh well.  But there is substantial likely-quite-usable work here, and it was generated almost entirely in a lazy fun experience while listening to an audiobook, barely thinking hard about the underlying code and just following the general vibe of programming.   And all that prompting vibe? - it's getting automated too, soon enough. 

So - nice work GPT4!  (and 4o)  Bummer we didnt build an entire emulator in one night, but maybe next time.  Passing to you for closing thoughts:
```

GPT4:
```
It sounds like your experiment was a fascinating exploration into the capabilities of GPT-4 for generating substantial and potentially functional code with minimal effort. Here are some closing thoughts on the project:

Achievement Highlights:

Code Generation: Successfully generated a significant amount of code for a Game Boy emulator, including memory controllers and opcode implementations. This is a testament to GPT-4's ability to produce code at scale.
Learning and Insight: Gained valuable insights into the potential and limitations of using AI for complex coding tasks. The experiment demonstrated that while GPT-4 can handle a lot of the grunt work, there are still areas where human oversight and debugging are crucial.
Proof of Concept: Established a strong foundation for a Game Boy emulator that can be built upon and refined further. The generated code provides a solid starting point for future development and debugging.
Reflections on the Process:

Prompting Strategy: Your approach of keeping the prompts simple and straightforward worked well to generate a large volume of code quickly. However, more complex and specific prompts might be necessary to fine-tune the implementation and handle edge cases.
AI Assistance: The experiment showed that AI can significantly accelerate the coding process, making it feasible to tackle large projects with less mental effort. However, the AI's output still requires validation and testing.
Potential for Automation: There is a clear potential to automate the meta-prompting process further, creating a more efficient workflow for generating and refining code with AI assistance.
Next Steps:

Debugging and Testing: The next phase of the project will involve rigorous debugging and testing. Using automated testing tools and integrating test suites like the Moonwalking Test Suite for Game Boy emulators can help identify and fix issues.
Architectural Refinements: Revisiting the architecture, especially the opcode handling, could improve the emulator's performance and maintainability. This might involve restructuring the code to follow a more modular and scalable design.
Collaboration and Tools: Leveraging tools like DevOps pipelines, continuous integration (CI) systems, and collaboration platforms could streamline the development process and ensure consistency across the codebase.
Broader Implications:

AI in Software Development: This experiment underscores the evolving role of AI in software development, where AI can assist with generating boilerplate code, handling repetitive tasks, and even suggesting architectural improvements.
Future of Coding: As AI capabilities continue to advance, the line between human and machine coding efforts will blur, enabling developers to focus more on creative and complex problem-solving while relying on AI for implementation details.
In conclusion, while the project did not result in a fully functional emulator, it achieved a significant milestone in demonstrating the potential of AI-assisted coding. The work completed lays a strong foundation for future development, and with continued effort, a fully functional emulator is within reach. The experience also provided valuable insights into how to better leverage AI for complex coding projects in the future. Great job on pushing the boundaries and exploring what's possible with GPT-4!
```
