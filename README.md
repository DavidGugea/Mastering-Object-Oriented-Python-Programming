# Mastering Object Oriented Python Programming


## Section 1: Tighter Integration Via Special**

## 1. Preliminaries, Tools, and Techniques

## 2. The ```__init__()``` Method

## 3. Integrating Seamlessly - Basic Special Methods

## 4. Attribute Access, Properties, and Descriptors

## 5. The ABCs of Consistent Design

## 6. Using Callable and Contexts

## 7. Creating Containers and Collections

## 8. Creating Numbers

## 9. Decorators and Mixins - Cross-Cutting Aspects

---

## Section 2: Object Serialization and Persistence

## 10.  Serializing and Saving - JSON, YAML, Pickle, CSV and XML

## 11. Storing and Retrieving Objects via Shelve

## 12. Storing and Retrieving Objects via SQLite

## 13. Transmitting and Sharing Objects

## 14. Configuration Files and Persistence

--- 

## Section 3: Object-Oriented Testing and Debugging

## 15. Design Principles and Patterns

## 16. The Logging and Warning Modules

## 17. Designing for Testability

## 18. Coping with the Command Line

## 19. Module and Package Design

--- 
---

# Chapter 2. The ```__init__()``` Method

### The implicit superclass - object and  the ```__init__()``` method

The base class of all classes is the ```object``` class. This class doesn't have an ```__init__()``` method, and it doesn't do much.

When an object is created in Python, an empty object is firstly created and then python calls the ```__init__()``` method to set the state ( the properties, etc. ) to the object. This is the method that creates the object's instance variables and perfroms any other one-time processing.

### Factory functions

In Python there are 2 common ways of building factories:

1. You create a function that creates objects of a certain class
2. You create a class that contains multiple methods for creating objects

Here is an example of using the first method:

```Python
def card(rank: int, suit: "Suit") -> "Card":
    """This is a factory method."""
    if rank == 1:
        return AceCard("A", suit)
    elif 2 <= rank < 11:
        return Card(str(rank), suit)
    elif 11 <= rank < 14:
        name = {11: "J", 12: "Q", 13: "K"}[rank]
        return FaceCard(name, suit)

    raise Exception("Design Failure")
```

The problem with this example is the **vague else clause**. On one hand, some ```else``` clause conditions are very obvious, on the other hand, if left unspecified, they might lead to bugs that are very hard to fix. **You should always avoid the vague else clause**.

**It's always  better to be explicit than implicit**. ( Read Zen Of Python )

> We should not force the reader to deduce a complex condition for an else clause. Either the condition sohluld be obvious, or it should be explicit.
> Catch-all else should be used rarely. Use it only when the condition is obvious. When in doubt, be explicit and use ```else``` to raise an exception. Avoid the vauge ```else``` clause.

You can use 2 common factory design patterns in factory functions:

1. An if-elif sequence
2. A mapping

For the sake of simplicity, you should only focus on one of these techniques. Avoid mixing them.

An if-elif sequence would look like this:

```Python
def card(rank: int, suit: "Suit") -> "Card":
    """Simplicity and consistency using elif sequences"""

    if rank == 1:
        return AceCard("A", suit)
    elif 2 <= rank < 11:
        return Card(str(rank), suit)
    elif rank == 11:
        return FaceCard("J", suit)
    elif rank == 12:
        return FaceCard("Q", suit)
    elif rank == 13:
        return FaceCard("K", suit)
    else:
        raise Exception("Design Failure")
```

If you would want to use a mapping factory design pattern, it would look like this:

```Python
def card(rank: int, suit: "Suit") -> "Card":
    """Simplicity using mapping and class objects"""
    class_ = {1: AceCard, 11: FaceCard, 12: FaceCard, 13: FaceCard}.get(rank, Card)
    return class_(str(rank), suit)
```

You can also use **two parallel mappings**:

```Python
def card(rank: int, suit: "Suit") -> "Card":
    """Two parallel mappings"""
    class_ = {1: AceCard, 11: FaceCard, 12: FaceCard, 13: FaceCard}.get(rank, Card)
    rank_str = {1: "A", 11: "J", 12: "Q", 13: "K"}.get(rank, str(rank))

    return class_(rank_str, suit)
```

You can map to a tuple of values:

```Python
def card(rank: int, suit: "Suit") -> "Card":
    """Mapping to a tuple of values"""
    class_, rank_str = {
        1: (AceCard, "A"),
        11: (FaceCard, "J"),
        12: (FaceCard, "Q"),
        13: (FaceCard, "K"),
    }.get(rank, (Card, str(rank)))

    return class_(rank_str, suit)
```

You can also use a parital function using ```lambda```:

```Python
def card(rank: int, suit: "Suit") -> "Card":
    """The partial function solution"""
    class_rank = {
        1: lambda suit: AceCard("A", suit),
        12: lambda suit: FaceCard("J", suit),
        13: lambda suit: FaceCard("Q", suit),
        14: lambda suit: FaceCard("K", suit),
    }.get(rank, lambda suit: Card(str(rank), suit))

    return class_rank(suit)
```

A ***Fluent API*** is an API that can call itself. Something like the ```Builder()``` method from **lombok, Java**. An example:

```Factory.build().add(obj1).add(obj2).saveToList()```

So the idea of a ***Fluent API*** is that each method returns the object itself.
Here is an example of a factory api implemented in python using the fluent api concept:

```Python
class CardFactory:
    """FLUENT API FOR FACTORIES"""
    def rank(self, rank: int) -> 'CardFactory':
        self.class_, self.rank_str = {
            1: (AceCard, "A"),
            11: (FaceCard, "J"),
            12: (FaceCard, "Q"),
            13: (FaceCard, "K"),
        }.get(
            rank, (Card, str(rank))
        )

        return self

    def suit(self, suit: "Suit") -> "Card":
        return self.class_(self.rank_str, suit)
```

You can see that each method returns itself.

Looking back at the ```__init__()``` method, we could implement the ```__init__()``` method in each sub-class of the class ```Card```. We still have to think about the ```DRY ( Don't repeat yourself ) principle.

Here is an example where we repeat the implement the ```__init__()``` method inside sub-classes and make the factory function easier:

```Python
class Card3:
    def __init__(self, rank: str, suit: Suit, hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft


class NumberCard3(Card3):
    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(str(rank), suit, rank, rank)


class AceCard3(Card3):
    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__("A", suit, 1, 11)


class FaceCard3(Card3):
    def __init__(self, rank: int, suit: Suit) -> None:
        rank_str = {11: "J", 12: "Q", 13: "K"}[rank]
        super().__init__(rank_str, suit, 10, 10)
```

This is how this implementation has made the factory function easier:

```Python
def card10(rank: int, suit: Suit) -> Card3:
    if rank == 1:
        return AceCard3(rank, suit)
    elif 2 <= rank < 11:
        return NumberCard3(rank, suit)
    elif 11 <= rank < 14:
        return FaceCard3(rank, suit)
    else:
        raise Exception("Rank out of range")
```

> We can see from this variation that we've created rather complex ```__init__()``` methods for a relatively minor improvement in the simplciity of a factory function. This is a common trade-off. **The complexity cannot be removed; it ca only be encapsulated**. The real question is how should responsibility be allocated for this complexity?
> **Factory functions encapsulate complexity.** There's a trade-off that occurs between sophisticated ```__init__()``` methods and factory functions. It's often better to push complex constructors into factory functions. A factory function helps separate construction and inital state-from-state change or other processing concerns.


### Composite Objects

A composite object is a container. You can design containers in different ways:

1. Wrap: you can wrap the collection of items that you want to store inside a class with a simplified interface. This is an example of the **Facade pattern**.
2. Extend: You can extend an existing collection class and add the items in the class itself

Example for wrapping:

```Python
class Deck:
    """Wrapping a collection class"""

    def __init__(self) -> None:
        self._cards = [card(r + 1, s) for r in range(13) for s in iter(Suit)]
        random.shuffle(self._cards)

    def pop(self) -> Card:
        return self._cards.pop()
```

Example for extending an already existing collection class:

```Python
class Deck2(list):
    """Extending a collection class"""

    def __init__(self) -> None:
        super().__init__(
            card(r + 1, s)
            for r in range(13) for s in iter(Suit)
        )
        random.shuffle(self)
```

### Stateless objects without ```__init__()```

In Python, classes can also be created without an ```__init__()``` method. These types of objects that are created from classes without the ```__init__()``` method are called **stateless objects**, since they weren't given a state at when after they were created.

### Abstract methods

If you want to build an abstract method you will have to use the ```@abstractmethod``` decorator from the ```abc``` module ( [Module docs](https://docs.python.org/3/library/abc.html) ).

> A decorator indicating abstract methods. Using this decorator requires that the class’s metaclass is ABCMeta or is derived from it. A class that has a metaclass derived from ABCMeta cannot be instantiated unless all of its abstract methods and properties are overridden. 

Example:

```Python
class BettingStrategy2(metaclass=ABCMeta):
    @abstractmethod
    def bet(self) -> int:
        return 1

    def record_win(self) -> None:
        pass

    def record_loss(self) -> None:
        pass
```

### Overloaded methods

When it comes to method overloading, you will have to use the ```@overload``` decorator from the ```typing``` module since ```mypy``` won't recognize it by default.

Example:

```Python
class Hand4:
    @overload
    def __init__(self, arg1: "Hand4") -> None:
        pass

    @overload
    def __init__(self, arg1: "Hand4", arg2: Card, *, split: Card) -> None:
        pass

    @overload
    def __init__(
            self,
            arg1: Union["Hand4", Card],
            arg2: Optional[Card] = None,
            arg3: Optional[Card] = None,
            arg4: Optional[int] = None
    ) -> None:
        pass
```

**The ```@overload``` decorator information is used by ```mypy```. It provides documentation for people using this class. It has no runtime impact.**

### Static, class-level, classmethod

In python you can create methods using 3 ways:

1. Static methods.
2. Class methods.
3. Instance methods

Static methods are methods that have nothing to do with the instances of the class and they can be called directly using the class name. In order to build a static method you need the ```@staticmethod``` decorator.

Example:

```Python
class Test:
    @staticmethod
    def test_static_method():
        print("You've called the static method")

Test.test_static_method() # Output : You've called the static method
```

Class methods are methods that can also be called either by the class itself or by instances of the class. It needs one argument as the first argument, and that is the class itself ( ```cls``` ). In order to build a class method you will need the ```@classmethod``` decorator.

Example:

```Python
class TestClass:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    @classmethod
    def test_class_method(cls):
        print(repr(cls))
```

The instance methods are the normal methods that can only be used with instances of the class.

### Privacy in Python

> Python's notion of privacy is simple:
> * Attributes and methods are all essentially public. The source code is available
> * Conventionally, we treat some names in a way that's less public. They're generally implementation details that are subject to change without notice, but there's no formal notion of private
 
In Python, names that begin with ```_``` are treated less public by some parts of Python. The ```help()``` function will hide these methods/properties.
Python's internal names begin and end with double underscores ```__``` and they are called dunder. The ```__init__()``` method is called dunder init. 

> Furhter, there's no benefit to trying to use ```__``` to create a truly private attribute or method in our code. All that happens is that we create a potential future problem if a release of Python ever starts using a name we chos efor internal purpose. Also, we're likely to run afoul of the internal name mangling that is applied to these names.
> The rules for the visibility of Python names are as follows:
> * Most names are public
> * Names that start with ```_``` are somewhat less public. Use them for implementation details that are truly subject to change
> * Names that begin and end with ```__``` are internal to Python. We never make these up; we only use the names define by the language reference.