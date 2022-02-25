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

```typescript [1-2|3-9|10-14]
// Explicit primitive annotation
const isAnExample: boolean = true;

// Object interface
interface Student {
  isEnterprise: boolean;
  enrollmentIds: number[];
  name: string;
}

// Function annotation
function logStudentName(student: Student): void {
  console.log(student.name);
}
```

---

## Basics (continued)

TypeScript uses a "structural" type system.

```typescript [1-8|1-12|1-15|]
interface Student {
  name: string;
}

interface Nanodegree {
  name: string;
  key: string;
}

function logStudentName(student: Student): void {
  console.log(student.name);
}

const student: Student = { name: "Casey" };
const nd: Nanodegree = { name: "TS Basics", key: "nd1" };

logStudentName(student); // OK
logStudentName(nd); // Also OK
```

---

## Narrowing 101

> [T]he process of refining types to more specific types than declared is called narrowing.

[TS Docs: Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)

---

## Narrowing 101

```typescript [1-3|1-7|]
function logAString(s: string): void {
  console.log(s);
}

const item: unknown = "abc";

logAString(item); // Error here

if (typeof item === "string") {
  logAString(item); // No error here
}
```

---

## TypeScript unions

```typescript []
type Thing = number | string | boolean;

const things: Thing[] = [1, "a", true, NaN];
```

---

## TypeScript unions

Also useful for optional properties...

```typescript []
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

```typescript [1-4|6-8|]
// Usually as a result of `map`ping an optional property
const maybeValues: (number | undefined)[] = [
  123, 456, undefined, 789
];

function fancyAlgorithm(x: number): number {
  return x + 1;
}

// Expected error: `number` vs `number | undefined`
maybeValues.map(fancyAlgorithm);
```

---

## Problem 1: Filter

A logical solution would be to try `filter`ing...

```typescript [1-7|9-11]
const maybeValues: (number | undefined)[] = [
  123, 456, undefined, 789
];

function fancyAlgorithm(x: number): number {
  return x + 1;
}

maybeValues
  .filter((maybeValue) => maybeValue !== undefined)
  .map(fancyAlgorithm); // No luck :(
```

---

## Problem 1: Filter

Looking at the basic definition of `filter` shows why:

```typescript [1|3-5|]
  filter(
    predicate: (val: T, i: number, array: T[]) => unknown,
    thisArg?: any,
  ): T[];
```

We provide `T[]` and get back `T[]` (not unreasonably).

---

## Problem 1: Filter

Enter custom type guards...

```typescript [1|1-5|1-7|]
type MaybeNumber = number | undefined;

function isDefinedNumber(n: MaybeNumber): n is number {
  return n !== undefined;
}

const maybeNumber: MaybeNumber = [1, undefined, 3, 4][0];

if (isDefinedNumber(maybeNumber)) {
  // type of maybeNumber is narrowed to `number`
  // within this block
  console.log("I am a number:", maybeNumber);
}
```

---

## Problem 1: Filter

Revisiting our problem...

```typescript [1-8|10-12|14-17]
// Same type guard and array
type MaybeNumber = number | undefined;
function isDefinedNumber(n: MaybeNumber): n is number {
  return n !== undefined;
}
const maybeValues: (number | undefined)[] = [
  123, 456, undefined, 789
];

function fancyAlgorithm(x: number): number {
  return x + 1;
}

maybeValues
  // .filter(maybeValue => maybeValue !== undefined)
  .filter(isDefinedNumber)
  .map(fancyAlgorithm); // No error...Hooray!
```

---

# Problem 2: Concepts and Labs living together (mass hysteria!)

---

## Problem 2: Concepts & Labs

[A Classroom Example](https://learn.udacity.com/nanodegrees/nd000/parts/dc13bd39-6568-4ab3-9dd2-56da21ebcd7e/lessons/ceac532e-8e5b-4dce-8e52-ee1f76593c8d/concepts/7bf75254-02ed-4e92-a841-b5749b6a4f36)

(`6e03fa06-101c-11ec-9081-bf993a04dadc`)

- Labs and Concepts require different UX flows...
- But sometimes we want to treat them as generic "lesson content"

So we sometimes want two different types...but sometimes want a single union type

---

## Problem 2: Concepts & Labs

As a first approach, we can just store labs and concepts separately...

```typescript [1-11|13-16]
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
```

---

## Problem 2: Concepts & Labs

```typescript []
const getPathToNextFromConcept = (
  currentKey: string, lesson: Lesson
) => {
  // concept is in lesson.concepts and not last item?
  //   return the next concept
  // is the last item?
  //   is there a lab?
  //     if so, return the lab path
  //     if not, send to the next lesson
};

const getSidebarLinks = (lesson: Lesson) => {
  // Combine:
  // lesson.concepts.map(getConceptLink)
  // lesson.lab ? getLabLink(lesson.lab) : null
};
```

---

## Problem 2: Concepts & Labs

This approach works, but:

1. We now have embedded business logic about the order of concepts => labs in multiple places
2. Similarly, we have embedded the [0, 1] labs per lesson assumption
3. We have to remember to handle both whenever we use lesson content

---

## Problem 2: Concepts & Labs

Ideally, we would have something like:

```typescript [1-8|10-12]
type Content = Concept | Lab;

const getContent = (lesson: Lesson): Content[] => {
  const { concepts } = lesson;
  const labs = lesson.lab ? [lesson.lab] : [];

  return [...concepts, ...labs];
};

const getPath = (content: Content): string => {
  // etc etc etc
};
```

But now we need a way to narrow Concepts/Labs

---

## Problem 2: Concepts & Labs

Perceptive listeners will recognize that this example is really about _creating_ a union type rather than narrowing it!

But if we accept that a union could be a useful readability improvement, then we need a way to narrow it. :)

---

## Problem 2: Concepts & Labs

We _could_ use type guards again.

```typescript []
interface Concept {
  // ...
  atoms: object[];
}

interface Lab {
  // ...
  workspaceKey: string;
}

const isConcept = (c: Concept | Lab): c is Concept => {
  // `return 'atoms' in c` ?
  // `!(return 'workspaceKey' in c)` ?
};
```

---

## Problem 2: Concepts & Labs

- There isn't an obvious "right" way to differentiate the two
- We could pick arbitrary properties, but now we need to keep the type guard synced with some arbitrary collection of properties
- Hold these thoughts; there's a better solution coming

---

# Problem 3: A Course by any other name

> What's in a name?

---

## Problem 3: Courses

- The Classroom supports both paid and free courses
- The data structures underlying both are similar or identical
- We have type definitions for both - largely as a documentation tool

```typescript []
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

![](https://i.kym-cdn.com/entries/icons/original/000/023/397/C-658VsXoAo3ovC.jpg)

---

## Problem 3: Courses

```typescript [1-2|4-13|15-17]
const freeCourseSideEffect = (fc: FreeCourse) => {};
const paidCourseSideEffect = (pc: PaidCourse) => {};

// We generate two courses with accurate annotations
const paidCourse: PaidCourse = {
  key: "paid-1",
  title: "A paid course",
};

const freeCourse: FreeCourse = {
  key: "free-1",
  title: "A free course",
};

// No type errors :(
freeCourseSideEffect(paidCourse);
paidCourseSideEffect(freeCourse);
```

---

## Problem 3: Courses

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

```typescript [1-7|9-17]
interface NewFreeCourse extends FreeCourse {
  _brand: "FreeCourse";
}

interface NewPaidCourse extends PaidCourse {
  _brand: "PaidCourse";
}

const newFreeCourse = {
  _brand: "FreeCourse" as const,
  ...freeCourse,
};

const newPaidCourse = {
  _brand: "PaidCourse" as const,
  ...paidCourse,
};
```

---

## Problem 3: Courses

...and our problem is solved.

```typescript []
const freeCourseSideEffect = (fc: NewFreeCourse) => {};
const paidCourseSideEffect = (pc: NewPaidCourse) => {};

// Yay, we have type errors...
freeCourseSideEffect(newPaidCourse);
paidCourseSideEffect(newFreeCourse);

// And no type errors here
paidCourseSideEffect(newPaidCourse);
```

---

## Problem 3: Courses

We could even encapsulate this type branding into a generic type.

```typescript []
interface Branded<UniqueBrand> {
  _brand: UniqueBrand;
}

interface NewFreeCourse extends
  Branded<"FreeCourse">, FreeCourse {}
interface NewPaidCourse extends
  Branded<"PaidCourse">, PaidCourse {}
```

---

## Problem 3: Courses

Naming things is hard.

- This example uses `_brand`
- The [TS Docs](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#discriminated-unions) use `kind`
- [TS Deep Dive](https://basarat.gitbook.io/typescript/main-1/nominaltyping#using-interfaces) uses `_[name]Brand` for a similar effect (as does the [TS repo](https://github.com/Microsoft/TypeScript/blob/7b48a182c05ea4dea81bab73ecbbe9e013a79e99/src/compiler/types.ts#L693-L698))

Ideally, the brand key wouldn't collide with potential values in the underlying type. Pick something reasonable, and be consistent.

---

## Problem 3: Courses

We can now use a discriminated union and don't really even need custom type guards.

```typescript []
const courses: (NewFreeCourse | NewPaidCourse)[] = [];

courses.forEach((course) => {
  if (course._brand === "FreeCourse") {
    // type: NewFreeCourse
  } else {
    // type: NewPaidCourse
  }
});
```

---

## Problem 3: Courses

- Note that we have made a run-time change here!
- This is helpful in our case because we want to be able to narrow the union.
- If it isn't helpful in your case, you can work solely through the type system to achieve type safety without run-time modifications.
- None of these techniques are difficult -- just be sure to match the tool to your use case.

---

## Branding

If you want to work solely within the type system...

```typescript [1-2|1-9|11-12|14-15|17-18]
enum FreeBrand { _ = "" }
enum PaidBrand { _ = "" }

interface FreeCourse extends Branded<FreeBrand> {
  key: string;
}
interface PaidCourse extends Branded<PaidBrand> {
  key: string;
}

const freeCourse = { key: "abc" } as FreeCourse;
const paidCourse = { key: "xyz" } as PaidCourse;

const freeCourseSideEffect = (fc: FreeCourse) => {};
const paidCourseSideEffect = (pc: PaidCourse) => {};

freeCourseSideEffect(paidCourse); // Error!
paidCourseSideEffect(paidCourse); // No error!
```

## Branding

- `enum`s offer a degree of nominal typing.
- As long as the names differ, the types are considered different.
- This approach requires asserting the type

---

## More branding!

Don't even need to use interfaces/objects...

```typescript [1-2|4-5|7-8]
enum LessonIdBrand { _ = "" }
type LessonId = LessonIdBrand & string;

enum NanodegreeIdBrand { _ = "" }
type NanodegreeId = NanodegreeIdBrand & string;

const lessonId: LessonId = "a-lesson" as LessonId;
const nanodegreeId: NanodegreeId = "a-nd" as NanodegreeId;
```

---

## Recap

- Union types are helpful, but inevitably we want to narrow them.
- Discriminated unions and type guards are a good first step.
- Be clear about your run-time vs compile-time needs
  - Only compile-time checks? Enum brands are a great solution.
  - Run-time checks? Adding a string const to the object might be best.

---

## Resources

[419-comment TS repo thread on nominal typing](https://github.com/Microsoft/TypeScript/issues/202)

[TypeScript Deep Dive: Nominal Typing](https://basarat.gitbook.io/typescript/main-1/nominaltyping)

[Nominal typing techniques in TypeScript](https://michalzalecki.com/nominal-typing-in-typescript/#approach-2-brands)

---

## More Resources (TS Docs)

[Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)

[Narrowing: control flow analysis](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#control-flow-analysis)

[Narrowing: using type predicates](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#using-type-predicates)

[Narrowing: discriminated unions](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-func.html#discriminated-unions)
