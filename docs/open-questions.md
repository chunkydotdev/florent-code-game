# Open questions

Things we don't know, with how we'd find out. Move an answer into
[game-model.md](game-model.md) once it's verified, and delete it from here.

## Blocking — need answers before we can build

- [ ] What language and runtime does the bot run in?
- [ ] What is the tick/turn model, and what compute budget do we get per tick?
- [ ] What does the state object we receive each tick contain?
- [ ] What is the full action space?
- [ ] How is a submission deployed, and how quickly does a new version reach the ladder?
- [ ] Can we run matches locally / offline against our own previous versions?

## Important — shapes strategy

- [ ] How is ladder rating computed, and how many matches does a change need to show up?
- [ ] Are matches 1v1 or many-player?
- [ ] Can we see replays of our matches, and of other people's?
- [ ] What are the prize categories? (they may reward something other than raw ladder rank)
- [ ] Team size limits — is this a solo entry or do we need teammates?

## Nice to know

- [ ] Is there a public API for ladder standings we could poll?
- [ ] Rate limits or cooldowns on redeploying?
