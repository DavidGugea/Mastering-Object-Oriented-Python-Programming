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

Class methods are methods that can also be called either by the class itself or by instances of the class. It needs one argument as the first argument, and that is the class itself ( ```mcs``` ). In order to build a class method you will need the ```@classmethod``` decorator.

Example:

```Python
class TestClass:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    @classmethod
    def test_class_method(mcs):
        print(repr(mcs))
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

# 3. Integrating Seamlessly - Basic Special Methods

In this chapter we'll go over the basic special methods. Special methods in python are methods that contain two underscores at the start and the beginning of their names. These are built-in methods that are called with built-in functions. Integrating these special methods and knowing how they work and how to change them will help make the code easier to write, understand and maintain. An example of a special method would be the ```__str__()``` method. These special methods are also called **dunder** methods ( double-underscore ). The ```__str__()``` ( dunder string ) is called whenever you write ```str(obj)``` on an object. Every object can override the ```__str__()``` method.

## The ```__repr__()``` and ```__str__()``` methods

Every object has 2 types of string representation. These are the ```__repr__()``` ( representation ) method and the ```__str__()``` ( string ) method.

* The ```__str__()``` method is used for a simple string representation that can be used anywhere. This must be a string representation that is easy for humans to read and comprehend. 
* The ```__repr__()``` method is a technical string representation and uses a complete Python expression to rebuild an object. 
    * The documentation for the ```__repr__()``` method states as following:
    * > If at all possible, this should look like a valid Python expression that could be used to recreate an objec twith the same value ( given an appropiate environment )
* The buid-in ```print()``` function for example, uses the object's ```__str__()``` method.
* When formatting an object inside of a string you can choose if you want to use the ```__str__()``` or the ```__repr__()``` method. Example: ```{x!r}``` uses the ```__repr__()``` method while ```{x!s}``` uses the ```__str__()``` method of the object.

There are usually 2 design cases where we have to override ```__str__()``` and ```__repr__()```:

* **Simple objects**: A simple object doesn't contain a collection of other objects and generally doesn't involve very complex formatting
* **Collection objects**: An object that contains a collection involves somewhat more complex formatting

Here is an example in code:

```Python
class TestClass:
    def __init__(self, value1: int, value2: int) -> None:
        self.value1 = value1
        self.value2 = value2

    def __str__(self) -> str:
        return "This is the __str__() method of the object"

    def __repr__(self) -> str:
        return "This is the __repr__() method of the object"

test_class = TestClass(1, 2)
print(f"{test_class!r} < --- > {test_class!s}")

# Output : This is the __repr__() method of the object < --- > This is the __str__() method of the objec
```

## The ```__format__()``` method

The ```__format__()``` method is used by the:

* ```f```-strings
* ```str.format()``` method
* ```format()``` method

All 3 of these functions are used to format an object.

You can also give arguments to a ```__format__()``` method. It looks like this:

```Python
"{0:<spec>}".format(some_object)
```

or:

```Python
f"{some_object:<spec>}"
```

```spec``` in this case stays for **specification** and this is how the ```__format__()``` method would pick up on that argument:

```Python
class TestClass:
    def __init__(self, value1: int, value2: int) -> None:
        self.value1 = value1
        self.value2 = value2

    def __format__(self, format_specification: str) -> str:
        print(format_specification)
        return ""
    

test_class = TestClass(1, 2)
print("{0:this is the format specification}".format(test_class))

# Output: this is the format specification
```

It is very important to know that if you are transforming a string inside the formatting string, you will not get the ```__format__()``` method invoked. You will invoke the method that you are using to transform your object into. 
If you use the ```{some_object!r}```, in this case, you will not use the ```__format__()``` method, you will use the ```__repr__()``` method because you are transforming the string inside the format.

You can also nest the formatting specifications:

```Python
test1 = 6
test2 = "a"
print(f"{test2:<{test1}}")
# Output:
# a      space
```

You can also delegate the ```__format__()``` method if your object is a container. You can delegate the ```__format__()``` to every item from your collection:

```Python
from typing import Any


class TestClass:
    def __init__(self, *items: Any) -> None:
        self.items = list(items);

    def __format__(self, format_specification: str) -> str:
        if format_specification == "":
            return str(self)

        return ", ".join(f"{c:{format_specification}}" for item in self.items)
```

## The ```__hash__()``` method

> The default ```__hash__()``` implementation inherited from an object reutnrs a value based on the object's internal ID value. This vlaue can be seen with the ```id()``` function.

So the ```__hash__()``` method returns a value based on the ```id()``` method.

> Not every object should provide a hash value. Speicifcally, if we're creating a class of stateful, **mutable** objects, the calss hould *never* return a hash value. There should not be an implementation of the ```__hash__()``` method. **It's bad to have object that claim to be equal and have different hash values**

There are 3 tiers of equality comparision:

* **The same hash value**: This mean taht two object **could** be equal. The has value provides us with a quick check for likely equality. If the has value is different, the two object cannot possibly be equal, nor can they be teh same object.
* **Compare as equal**: This mean that the hash values must also have been equal. This is the definition of hte ```==``` operator. The objects may be teh same object.
* **Same ID values**: This mean that they are the same object. They also compare as equal and will also have teh same hash value. This is the definition of the ```is``` operator.

> The **Fundamental Law of Hash ( FLH )** has two parts:
> * Objects that compare as equal have the same hash value.
> * Objects with the same hash value may actually be distinct and not compare as equal.

There are three use cases for defining equality tests and hash value via the ```__eq__()``` and ```__hash__()``` methods:

* **Immutable objects**: These are stateless objects of types such as tuples, namedtuples, and frozensets that cannot be updated. We have two choices:
    * Define neither ```__hash__()``` nor ```__eq__()```. This means doing nothing and using the inherited definitions. In this case, ```__hash__()``` returns a trivial function of the ID value for the object, and ```__eq__()``` compares the ID values.
    * Define both ```__hash__()``` and ```__eq__()```. Note that we're expected to define both for an immutable object.
* **Mutable objects**: These are stateful objects that can be modified internally. We have one design choice:
    * Define ```__eq__()``` but set ```__hash__()``` to ```None```. These cannot be used as ```dict``` keys or items in ```sets```.

## The ```__bool__``` method

In Python, empty lists, sets, dictionaries, values such as False, 0, or emtpy strings have a boolean value of ```False```. In cases when we design for example a container class, we might want to override the ```__bool__()``` method to be delegated to the ```__bool__()``` method of the collection that is stored in the container and not the container itself.

For example:

```Python
class Container:
    def __init__(self, items: Any) -> None:
        self._items = items

    def __bool__(self) -> bool:
        return bool(self._items)
```

## The ```__bytes__()``` method

The ```__bytes()__``` method is called when you use the ```bytes()``` built-in function. It is usually only overwritten when using serialization of objects for persistent storage or transfer.

## The comparision operator methods

| Operator | Special methods |
|----------|-----------------|
|```x < y```|```x.__lt__(y)```|
|```x <= y```|```x.__le__(y)```|
|```x == y```|```x.__eq__(y)```|
|```x != y```|```x.__ne__(y)```|
|```x > y```|```x.__gt__(y)```|
|```x >= y```|```x.__ge__(y)```|

> **Here are two basic rules**
> First, the operatnd on the lef-thand side of the operator is checked for an implementation : ```A<B``` means ```A.__lt__(B)````.
> Second, the operand on the right-hand side of the operator is checkc for a reversed implementation: ```A<B``` means ```B.__gt__(A)```. The rare exception to this occurs when the right-hand operand is a subclass of the left-hand operand; then, the right-hand operand is checked first to allows a subclass to override a superclass.

If you use ```obj1 > obj2``` and ```obj1``` doesn't have the ```__gt__()``` method implemented, python uses ```obj2.__lt__(obj1)``` instead.

The various comparision methods use two kinds of type checking: **class** and **protocol**:

* Class-based type checking uses ```isinstance()``` to check the class membership of the object. When the check fails, the method returns the special ```NotImplemented``` value; this allows the other operand to implement the comparison. The ```isinstance()``` check also informs mypy of a type constraint on the objects anemd in the expression.
* Protocol-based type checking follows **duck typing** principles. If the object supports the proper protocol, it will have the necessary attributes. This is shown in the implementation of the ```__le__()``` and ```__ge__()``` methods. A ```try```: block is used to wrap the attempt and provide a useful ```NotImplemented``` value if the protocl sin't available in the object. In this case, the ```cast()``` function is used to inform mypy that only objects with the expected class protocol will be used at runtime.

> Two classes are poolymorphic when they share common attributes and methods. One common example of this is objects of the ```int``` and ```float``` classes. Both have ```__add__()``` methods to implement the ```+``` operator. Another example of this is that most collections offer a ```__len__()``` method to ipmlement the ```len()``` function. The results are produced in different ways, depending on the implementation details.
> One symptom of **Pretty Poor Plymorphism** is the reliance on the ```isinstance()``` to determine the subclass memebership. Generally, this is a violation of the basic ideas of encapsulation and class design. A good set of polymorphic subclass definitions should be completely equivalent with the same methods signatures. Ideally, the calss definitions are also opaque; we don't need to look inside the class definition. A poor set of plymorphic classes uses extensive ```isinstance()``` class testing.

## The ```__del__()``` method

> The intent is to give an boject a chance to do any cleanup or finalization just before the boject is remove from memory. **This use case is handled much more cleanly by context manager objects and the ```with``` statement**.

The ```__del__()``` is never invoked at an easy-to-predict time. It is not always deleted when the object has 0 count of references, nor it is always deleted when you use the ```del``` method. In the case of a **memory leak** ( that is when the object has 0 coutn of references but it is still not deleted ), the ```__del__()``` method is never invoked, which can lead to problems that are very hard to debug. **For these reasons, a context manager is often preferable to implementing ```__del__()```.**

A circular reference is when you have a parent and a child object and they both have references to each other. So the parent object might be a container object that contains a collection with all the children and each child might have a property that points its parent. This is known as a ```circular reference```. The problem with circular references and the ```__del__()``` method is that we can't break the circularity by putting ocde in the ```__del__()``` method. The ```__del__()``` method is called **after** the circularity has been broken and the refenrece counts are already 0. When we have circular references, we can no longer rely on simple Pythonr eference counting to clear out the memory of unused objects. We must use a weak reference ( from the ```weakref``` module ).

The most common use for ```__del__``` is to ensure the files are closed ( this is done in a much cleaner way by using context managers ).

## The ```__new__()``` method

The ```__new__()``` method is where an uninitialized object is created prior to the ```__init__()``` method setting the attribute values of the object. 

> For any class we define, the default implementation of ```__new__()``` is inherited from the parent calss. Implicitly, the ```object``` object is the parent of all classes. The ```object.__new__()``` method build a simple, empty object of the reuqired class. The arguments and keyword to ```__new__()```, with the exception of the ```cls``` argument, are passed to ```__init__()``` as part of the standard Python behavior.
> The following are two cases when this default behavior isn't perfect:
> * When we want to subclass an immutable class definition. We'll look at this next.
> * When we needto create a metaclass. That's the subject of the next section, as it's fundamentally different from creating immutable objects.

The ```__new__()``` method can also be used to create metaclasses. **A metaclass is used to build a class**. Once a class object has been built, the class object is used to build instance objects.