## Hello

- Why are we here
  - 3 real-world problems from `learn-web`
  - Each involves a situation where a value may be one of multiple types
  - Easier => More difficult

---

## Today's theme

Simple tools for simple(r) code

---

## TypeScript basics in 60 seconds

```typescript
const isAnExample: boolean = true; // Explicit primitive annotation

// Object interface
interface Student {
  isEnterprise: boolean;
  enrollmentIds: number[];
  name: string;
}

function logStudentName (student: Student) {
  console.log(student.name);
}
```

---

## TypeScript basics in 60 seconds (continued)

TypeScript uses a "structural" type system.

```typescript
interface Student {
  id: number;
  name: string;
}

interface Nanodegree {
  id: number;
  name: string;
  version: string;
  key: string;
}

function logStudentName (student: Student) {
  console.log(student.name);
}

const student: Student = { id: 1, name: 'Casey' }
const nd: Nanodegree = { id: 1, name: 'TS Basics', version: '1.0.0', key: 'nd12345' }

logStudentName(student) // OK
logStudentName(nd) // Also OK
```

---

## TypeScript unions

```typescript
type Thing = number | string | boolean;

const things: Thing[] = [1, 'a', true, NaN]
```

Also useful for optional properties...

```typescript
interface Student {
  id: number;
  favoriteColor?: string; // string | undefined
}
```

---

# Problem 1: The case of the untrustworthy filter

(a warm-up activity)

---

## Problem 1: Filter

If you work with TS for long, you inevitably run into this problem:

```typescript
// Usually as a result of `map`ping an optional property...
const maybeValues: (number | undefined)[] = [
  123, 456, undefined, 789
]

function fancyAlgorithm (x: number) {
  return x + 1
}

// Expected error: `number` vs `number | undefined`
maybeValues.map(fancyAlgorithm)
```

---

## Problem 1: Filter

A logical solution would be to try `filter`ing...

```typescript
const maybeValues: (number | undefined)[] = [
  123, 456, undefined, 789
]

function fancyAlgorithm (x: number) {
  return x + 1
}

maybeValues
  .filter(maybeValue => maybeValue !== undefined)
  .map(fancyAlgorithm) // No luck :(
```

---

## Problem 1: Filter

Looking at the basic definition of `filter` shows why:

```typescript
  filter(
    predicate: (value: T, index: number, array: T[]) => unknown,
    thisArg?: any,
  ): T[];
```

We provide `T[]` and get back `T[]` (not unreasonably).

---

## Problem 1: Filter

Enter type guards...

```typescript
type MaybeNumber = number | undefined

function isDefinedNumber (n: MaybeNumber): n is number {
  return n !== undefined
}

const maybeNumber: MaybeNumber = 1

if (isDefinedNumber(maybeNumber)) {
  // type of maybeNumber is narrowed to `number` within this block
  console.log('I am a number:', maybeNumber)
}
```

---

## Problem 1: Filter

Revisiting our problem...

```typescript
// Same type guard
type MaybeNumber = number | undefined

function isDefinedNumber (n: MaybeNumber): n is number {
  return n !== undefined
}

// Same problem
const maybeValues: (number | undefined)[] = [
  123, 456, undefined, 789
]

function fancyAlgorithm (x: number) {
  return x + 1
}

// But now it works
maybeValues
  // .filter(maybeValue => maybeValue !== undefined)
  .filter(isDefinedNumber)
  .map(fancyAlgorithm) // No error...Hooray!
```
---

# Problem 2: Concepts and Labs living together (mass hysteria!)
---

## Problem 2: Concepts & Labs

[A Classroom Example](https://learn.udacity.com/nanodegrees/nd000/parts/dc13bd39-6568-4ab3-9dd2-56da21ebcd7e/lessons/ceac532e-8e5b-4dce-8e52-ee1f76593c8d/concepts/7bf75254-02ed-4e92-a841-b5749b6a4f36)

(for student `6e03fa06-101c-11ec-9081-bf993a04dadc`)

- Labs and Concepts require a different UI but are often treated as being "lesson content" in a general sense
- They represent different UX workflows
- Sometimes we want to treat them as generic "lesson content"

So we sometimes want two different types...but sometimes want a single union type

---

## Problem 2: Concepts & Labs

As a first approach, we can just store labs and concepts separately...

```typescript
interface Concept {
  key: string;
  title: string;
  atoms: object[];
}

interface Lab {
  key: string;
  title: string;
  workspaceKey: string;
}

interface Lesson {
  concepts: Concept[];
  lab?: Lab;
}

const getPathToNextFromConcept = (currentKey: string, lesson: Lesson) => {
  // currentConcept is in lesson.concepts and is not the last item?
  //   return the next concept
  // is the last item?
  //   is there a lab?
  //     if so, return the lab path
  //     if not, send to the next lesson
};

const getPathToNextFromLab = (currentKey: string, lesson: Lesson) => {
  // go to the next lesson
};

// Note that there is also getPathToPrev[x] for these!!!

const getSidebarLinks = (lesson: Lesson) => {
  // Combine:
  // lesson.concepts.map(getConceptLink)
  // lesson.lab ? getLabLink(lesson.lab) : null
};
```

This approach works, but:
1. We now have embedded business logic about the order of concepts => labs in multiple places
  a. similarly, we have embedded the [0, 1] labs per lesson assumption
2. We have to remember to handle both whenever we use lesson content
---

## Problem 2: Concepts & Labs

Ideally, we would have something like:

```typescript
const getContent = (lesson: Lesson): (Concept | Lab)[] => {
  const { concepts } = lesson;
  const labs = lesson.lab ? [lesson.lab] : [];

  return [...concepts, ...labs];
};

const getPath = (content: Concept | Lab): string => {
  // etc etc etc
};

const getPathToNext = (currentKey: string, lesson: Lesson) => {
  const content = getContent(lesson);
  const currentIndex = content.find(({ key }) => key === currentKey);
  // If content[currentIndex + 1] exists, call getPath on it
};
```

- This is easier to reason about
- But now we need a way to differentiate between Concepts and Labs
- So we're back to narrowing a union type

---
## Problem 2: Concepts & Labs

Perceptive listeners will recognize that this example is really about _creating_ a union type rather than narrowing it!

But if we accept that a union could be a useful readability improvement, then we need a way to narrow it. :)

---

## Problem 2: Concepts & Labs

We _could_ use type guards again.

```typescript
interface Concept {
  key: string;
  title: string;
  atoms: object[];
}

interface Lab {
  key: string;
  title: string;
  workspaceKey: string;
}

const isConcept = (content: Concept | Lab): content is Concept => {
  // `return 'atoms' in content` ?
  // `!(return 'workspaceKey' in content)` ?
};
```
- There isn't an obvious "right" way to differentiate the two
- We could pick arbitrary properties, but now we need to keep the type guard synced with some arbitrary collection of properties
- Hold these thoughts; there's a better solution coming

---

# Problem 3: A Course by any other name

> What's in a name? That which we call a course
> By any other name would preserve type safety;
- Shakespeare, probably

---

## Problem 3: Courses

- The Classroom supports both paid and free courses
- As you might imagine, the data structure underlying both is similar or identical
- We have type definitions for both - largely as a documentation tool

```typescript
export interface PaidCourse {
  readonly key: string;
  readonly title: string;
  readonly paidCourseOnlyProperty?: string;
}

export interface FreeCourse {
  readonly key: string;
  readonly title: string;
}
```

---

## Problem 3: Courses

```typescript
const freeCourseSideEffect = (fc: FreeCourse) => {
  console.log(`I am doing something with ${fc.title}`);
};

const paidCourseSideEffect = (pc: PaidCourse) => {
  console.log(`I am doing something with ${pc.title}`);
  console.log(`I can even use this: ${pc.paidCourseOnlyProperty}`);
};

// We generate two course objects with accurate type annotations
const paidCourse: PaidCourse = {
  key: 'paid-1',
  title: 'A paid course',
};

const freeCourse: FreeCourse = {
  key: 'free-1',
  title: 'A free course',
};

// No type errors :(
freeCourseSideEffect(paidCourse);
paidCourseSideEffect(freeCourse);
```

- This may be surprising if you are familiar with other type systems.
- TS uses a "structural" type system, not a "nominal" system
---

## Problem 3: Courses
- So this is worse than the previous problems
- Not only can we not use or narrow a union, the type safety here is merely an illusion
---

## Problem 3: Courses
Solution 1: keep them separate (manually) and be conscientious

Valid, but this resulted in some undesirable verbosity for us.
---
## Problem 3: Courses
Solution 2: Differentiate the types

```typescript

interface Branded<UniqueBrand> {
  _brand: UniqueBrand;
}

interface BrandedFreeCourse extends Branded<'FreeCourse'>, FreeCourse {}
interface BrandedPaidCourse extends Branded<'PaidCourse'>, PaidCourse {}

const brandedFreeCourse = {
  _brand: 'FreeCourse' as const,
  ...freeCourse,
}

const brandedPaidCourse = {
  _brand: 'PaidCourse' as const,
  ...paidCourse,
}

const brandedFreeCourseSideEffect = (fc: BrandedFreeCourse) => {
  console.log(fc.title);
};

const brandedPaidCourseSideEffect = (pc: BrandedPaidCourse) => {
  console.log(pc.title);
};

// Yay, we have type errors...
brandedFreeCourseSideEffect(brandedPaidCourse);
brandedPaidCourseSideEffect(brandedFreeCourse);

// And no type errors here
brandedPaidCourseSideEffect(brandedPaidCourse);

```

---
## Problem 3: Courses

We can now use a discriminated union and don't really even need custom type guards.

```typescript
const courses: (BrandedFreeCourse | BrandedPaidCourse)[] = []

courses.forEach(course => {
  if (course._brand === 'FreeCourse') {
    // type: BrandedFreeCourse
  } else {
    // type: BrandedPaidCourse
  }
})
```

---
## Problem 3: Courses

- Note that we have made a run-time change here!
- This is helpful in our case because we want to be able to narrow the union.
- If it isn't helpful in your case, you can work solely through the type system to achieve type safety without run-time modifications.
- None of these techniques are difficult -- just be sure to match the tool to your use case.
---
## Problem 3: Courses

If you want to work solely within the type system...

### This one weird trick compilers don't want you to know...

```typescript
enum FreeCourseBrand {}
enum PaidCourseBrand {}

interface UberBrandedFreeCourse extends Branded<FreeCourseBrand>, FreeCourse {}
interface UberBrandedPaidCourse extends Branded<PaidCourseBrand>, PaidCourse {}

const uberBrandedFreeCourse = {
  _brand: FreeCourseBrand,
  ...freeCourse,
}

const uberBrandedPaidCourse = {
  _brand: PaidCourseBrand,
  ...paidCourse,
}

const uberBrandedFreeCourseSideEffect = (fc: EnumBrandedFreeCourse) => {
  console.log(`I am doing something with ${fc.title}`);
};

const uberBrandedFreeCourseSideEffect = (fc: EnumBrandedFreeCourse) => {
  console.log(`I am doing something with ${fc.title}`);
};
```

---
## More branding!

TODO !!!

Don't even need to use interfaces/objects...

```typescript
enum LessonIdBrand {}
type LessonId = LessonIdBrand & string;

enum NanodegreeIdBrand {}
type NanodegreeId = NanodegreeIdBrand & string;

const lessonId: LessonId = 'a-lesson' as LessonId;
const nanodegreeId: NanodegreeId = 'a-nanodegree' as NanodegreeId;

const getLesson = (id: LessonId) => {
  console.log(`I am retrieving lesson "${id}"`)
}

getLesson(lessonId) // Good
getLesson(nanodegreeId) // Ummmmmmm?
// TODO: Add `_ = ""` to the brand enums
```

---
## Recap

- Be clear about your run-time vs compile-time needs
  - Only compile-time checks? Enum brands are a great solution.
  - Run-time checks? Adding a string const to the object itself has been a good solution for us.

---
