# Labeling Guide

## Contextual notes
Labels are created from a turn in a conversation log.
Each turn's speaker maps to an entity. Pronouns like I/me/my/you are interpreted relative to the corresponding entities
associated with the speaker transcript.

## "entity" label
### Definition
A unique person, animal, or organization, or a unique physical object.  
Organizations includes any group of people where they are organized enough to give their group a name, so this includes 
teams and clubs as well as companies and schools.  Entities must be used in a statement to be considered.

### Examples
The school board game club: yes
the kids' elementary school: yes
our family: no
school class 1-3: yes
my wife's friends: no
my wife: yes
our dog Berry: yes
older son's backpack: yes
my work laptop: yes
toilet paper: no

## "statement" extracted from conversation/transcript/speech

### Definition
Statements must be "about" one or more entities, and a must indicate a state that will still
be likely true for a while (e.g. tomorrow).  Examples include problems, personal relationships, ownership, needs.
There are two kinds of statements:
 kind: "fact" describes how things are, without an implied wish for change
 kind: "intent" includes explicit intentions, but also things stated as facts that the speaker would clearly wish to be differnet. 
 Intents have additional optional fields:
 - subject -- entity whose experience this is
 - issue -- that could motivate some kind of action
   - issue_status - OPEN/RESOLVED
 - goal -- an intended outcome or success criteria
   - goal_status - OPEN/DONE/DROPPED
 - next-step -- immediate approach

Subject is required.  It's possible for issue and goal to both be specified when recording a statement with kind="intent", 
but at least one them is necesary.  A problem without a known solution might not have a goal (I am losing my hair.). 
A goal to get an A might not involve any obvious issue.  Either way, next-step is possible but optional.
Issues (I am losing my hair) could have a next-step (talk to a doctor) without defining any concrete success criteria, 
and goals (getting an A) can define a next-step (studying for 2 hours) without invoking an issue.  In many cases, 
next-step is defined later in an update, rather than in the same statement that defined the issue.

### Examples:

My shoes are too tight
kind: intent ("too tight" indicates a problem to be addressed)
subject: me, issue: shoes are too tight, goal: unknown, next-step: unknown

Later: “Got new shoes” sets the shoe intent to RESOLVED. 

I need to email my brother.
kind: intent
subject: me, issue: unknown, goal: send email to my brother, next-step: unknown

My wife has a meeting on tuesday
kind: fact

I'm losing my hair
kind: intent (assuming the context implies the speaker wishes it different, which is usually the case)
subject: me, issue: losing hair, goal: unknown, next-step: unknown

If I don't call the school before 7, they will penalize us.
kind: intent (it's worded as a fact, but it's a clear statement of intention)
subject: me, issue: school could penalize us, next-step: call school before 7

"Can you pick up the milk?" 
kind: intent
subject: speaker-1, issue: "wants milk picked up", goal: unknown, next-step: unknown

(later response)
"Sure, it's on my way home"
new issue:
subject: speaker-2, issue: unknown, goal: "get milk", next-step: pick up on way home

"I put the milk in the fridge"
speaker-1 has issue_status=RESOLVED, speaker-2 has goal_status=DONE

Mark doesn’t know how to cook
kind: fact

Mark wants to learn to cook.
kind: intent
subject: mark, issue: unknown, goal: learn to cook, next-step: unknown

“Forget the cooking class” sets goal_status=DROPPED.

Ken says Yuki is moving
kind: fact (stored as a unit, we do not have entity-attribution yet, though the speaker-turn is referenced)

# Later:
We are deferring relationships between tasks
Goals can have alternative approaches (OR) and blockers (AND)
v1 stores only the chosen next action as text, when it's stated
next-steps are really subgoals chosen as part of an approach
and goals/issues/next-steps can be separated into related nodes instead of the current 1:1 mapping that's imposed,
where goals have a success criteria, and issues may not.
Can also one optional field on items for entity-attribution: attributed_to: entity ref | None,
which adds a statement/entity relationship.
This would cover the Ken said Yuki is moving example more structurally.  As it is, we just store the full text.
