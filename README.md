# Mastering Object Oriented Python Programming


## Section 1: Tighter Integration Via Special

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

# Section 1

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

# 4. Attribute Access, Properties and Descriptors

## Class and instance variables

Before getting into this chapter, I would like to talk about the difference between class and instance attributes. Instance attributes, as you know, are attributes that are implemented using the ```__init__()``` method. They look something like this:

```Python
class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
```

These are instance attributes. We've talked about classmethods ( they use the ```@classmethod``` decorator ) before and we've said that these methods can be used by the instances, but they can also be used by the class itself. 
Class attributes behave the same as class methods. Class attributes can be used by the instances, but they can also be used by the class itself. When you access a class attribute from an instance, python will look at that instance's namespace and if it won't find the attribute, it will look at the namespaces of the class.

Example of class attributes:

```Python
class Person:
    some_class_variable: int = 5

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age


test_person = Person("test_name", 23)
print(test_person.name)  # test_name
print(test_person.age)  # age 
print(test_person.some_class_variable)  # 5
print(Person.some_class_variable)  # 5
```

In this example we have 2 instance attributes ( name and age ) and 1 class attribute ( some_class_variable ). 
You can look at the attributes of a class using the ```dir()``` and ```vars()``` methods. The difference between ```dir()``` and ```vars()``` is that ```vars()``` returns the ```__dict__``` variable while ```dir()``` returns a list with all attributes that the class can access ( including attributes from super-classes )
The ```__dict__``` attribute of a class returns a dictionary that stores an object's writable attributes.

Example:

```Python
print(vars(test_person))
print(test_person.__dict__)
print(dir(test_person))

"""
Output:
{'name': 'test_name', 'age': 23}
{'name': 'test_name', 'age': 23}
['__annotations__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'age', 'name', 'some_class_variable']
"""
```

The ```__class__``` attribute of a class will return it's type. For example, in our case, ```test_person.__class__``` will return us the ```Person``` class.
This means that, internally, when you call an object's class variable, if python doesn't find that variable inside the object's namespace, it will go up the ladder, to it's type ( to it's class ) and look into that, and so on ( it works like the prototype chain in JavaScript ).

So, internally, this is what happens when you write ```test_person.some_class_variable```:

```Python
print(test_person.some_class_variable)
print(test_person.__class__.some_class_variable)
```

This returns the exact same result. 
But this also means that, if you change the class variable from the class itself, it will be changed for all instances, but if you change the class variable from an instance, it will only change for that perticular instance. That happens because you basically give the class a new attribute by dynamically implementing into into the namespaces of that object.

Example:

```Python
class Person:
    some_class_variable: int = 5

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

test_person_1 = Person("test_person_1_name", 23)
test_person_2 = Person("test_person_1_name", 24)

print(test_person_1.some_class_variable)
print(test_person_2.some_class_variable)
Person.some_class_variable = 20
print(test_person_1.some_class_variable)
print(test_person_2.some_class_variable)
print("-"*50)
test_person_1.some_class_variable = 30
print(test_person_1.some_class_variable)
print(test_person_2.some_class_variable)

"""
Output:
5 
5
20
20
--------------------------------------------------
30
20
"""
```

Class variables are widely used in descriptors and with the ```dataclass``` module.

## Optional attributes

Most of the time we create a collection of attributes in the ```__init__()``` method that describe certain state of the object. We provide names and ideally, default value, for all the attributes in the ```__init__()``` method

> While it's not required to place all the attributes in the ```__init__()``` method. While this is not required, it's the place ```mypy``` checks to gather the expected list of attributes of an object. An optional attribute can be used as part of an object's state, but there aren't easy ways to describe the absence of an attribute.
> An optional attribute also pushes the edge of the envelope in terms of class definition. A class is defined by the unique collection of attributes. Attributes are best added ( or removed  )by creating a subclass or superclass definition. Dynamic changes to the attributes are dconfusing to tools such as ```mypy``` as well as to people
> Generally, optional attributes imply a concealed or informal subclass relationship. Therefore, we bump up against Pretty Poor Polymorphism whne we use optional attributes. Mutliple polymorphic subclasses are often a better implementation than optinal attributes.

## Creating properties

The difference between an attribute and a property is that properties can implement setters getters and deleters.
There is also another difference between attributes and properties and that is that new attributes can always be dynamically added to the class, while new properties can't.
You can build a property by either using the ```@property``` decorator or the ```property()``` method.

When using the ```@property``` decorator, that describes the getter, then you will have to use the name of the attribute and then add *.setter* or/and *.deleter* for the setter and deleter. You can't, however, build a ```setter``` nor a ```deleter``` without have a ```getter``` first:

```Python
@property
def value(self) -> int:
    return self._value

@value.setter
def value(self) -> None:
    return self._value

@value.deleter
def value(self) -> None:
    print("You've deleted the value")
```

There are two basic design patterns for properties:

* Eager calculation: When we set a value via a property, other attributes are also computed
* Lazy calcuation: Calculation are deferred until requested via a property

Example of lazy and eager calculation:

```Python
class Hand:
    def __init__(
            self,
            dealer_card: BlackJackCard,
            *cards: BlackJackCard
    ) -> None:
        self.dealer_card = dealer_card
        self._cards = list(cards)

    def __str__(self) -> str:
        return ", ".join(map(str, self.card))

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"({self.dealer_card!r}"
            f"{', '.join(map(str(repr, self.card)))})"
        )


class Hand_Lazy(Hand):
    @property
    def total(self) -> int:
        delta_soft = max(c.soft - c.hard for c in self._cards)
        hard_total = sum(c.hard for c in self._cards)
        if hard_total + delta_soft <= 21:
            return hard_total + delta_soft

        return hard_total

    @property
    def card(self) -> List[BlackJackCard]:
        return self._cards

    @card.setter
    def card(self, a_card: BlackJackCard) -> None:
        self._cards.append(a_card)

    @card.deleter
    def card(self) -> None:
        self._cards.pop(-1)


class Hand_Eager(Hand):
    def __init__(
            self,
            dealer_card: BlackJackCard,
            *cards: BlackJackCard
    ) -> None:
        self.dealer_card = dealer_card
        self.total = 0
        self._delta_soft = 0
        self._hard_total = 0
        self._cards: List[BlackJackCard] = list()
        for c in cards:
            self.card = c

    @property
    def card(self) -> List[BlackJackCard]:
        return self._cards

    @card.setter
    def card(self, a_card: BlackJackCard) -> None:
        self._cards.append(a_card)
        self._delta_soft = max(a_card.soft - a_card.hard, self._delta_soft)
        self._hard_total = self._hard_total + a_card.hard
        self._set_total()

    @card.deleter
    def card(self) -> None:
        removed = self._cards.pop(-1)
        self.hard_total -= removed.hard
        self._delta_soft = max(c.soft - c.hard for c in self._cards)
        self._set_total()

    def _set_total(self) -> None:
        if self._hard_total + self._delta_soft <= 21:
            self.total = self._hard_total + self._delta_soft
        else:
            self.total = self._hard_total
```

In the eager computation case, each time a cardi s added via the card ```setter``` property, the ```total``` attribute is updated.

> In both cases, the client software uses the ```total``` attribute. The lazy implementation defers computation of total until required, but recomputes them every time. The eager implementation computes total immediately, and only recomputes them on a change to the hand. The trade-off is an important software engineering question, and the final choice depends on how the overall application uses the ```total``` attributes.

> The advantage of using properties is that the syntax doesn't change when the implementation changes. We can make a similar claim for ```getter/setter``` method functions. However, ```getter/setter``` method functions involve extra syntax that isn't very helpful or informative. The following are two example, one of which involves the use of a ```setter``` method, while the other uses the assignment operator:

```Python
obj.set_something(value)
obj.something = value
```

## Special methods for attribute access

The special methods used for attributes access are:

* The ```__setattr__(self, name, value)``` will **create and set** attributes
* The ```__getattr__(self, name)``` is a fallback method used when an attribute is not defined. The default behavior is the raise an ```AttributeError```
* The ```__getattribute(self, name)``` is called every time you access an attribute ( even if the attribute is part defined or not ).
* The ```__delattr__(self, name)``` method deletes an attribute

## Limiting attribute names with ```__slots__```

We can use ```__slots__``` in order to maek sure that no new attributes can be added to a class. Example:

```Python
class Person:
    __slots__ = ("name", "age")

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

test_person = Person("test_person_name", 23)
print(test_person.name)
print(test_person.age)
# test_person.new_instance_variable = 5  # AttributeError: 'Person' object has no attribute 'new_instance_variable'

```

> Settings the ```__slots__``` attribute turns off he internal ```__dict__``` featuer of the obejct and limits us to these attribute names only. The define attribute  values are mutable even though ne wattributes cannot be added.

## Dynamic attributes with ```__getattr__()```

As I've already said, the ```__geattr__(self, name)``` method is called whenever an attribute is not implemented. We can use this to our advantage to dynamically assign values to attributes that were not defined yet.

Example:

```Python
class RTD_Solver:
    def __init__(
            self, *,
            rate: float = None,
            time: float = None,
            distance: float = None
    ):
        if rate:
            self.rate = rate
        if time:
            self.time = time
        if distance:
            self.distance = distance

    def __getattr__(self, item: str) -> float:
        if item == "rate":
            return self.distance / self.tiem
        elif item == "time":
            return self.distance / self.rate
        elif item == "distance":
            return self.rate * self.time
        else:
            raise AttributeError(f"Can't compute {item}")
```

In this example, the ```RTD_Solver``` class only needs 2 attributes given and the third one will be implemented dynamically using the ```__getattr__(self, name)``` method.

> When an instance of ```RTD_Solver``` is created with an attribute value set by the ```__init__()``` method, the ```__getattr__()``` method is not used toe fetch the attribute. The ```__getattr__()``` method is only used for unknown attributes.

## Creating immutable obejcts as a ```NamedTuple``` subclass

The best approach in terms of creating immutable objects is using the ```typing.NamedTuple``` class as an upper-class.

Example:

```Python
from typing import NamedTuple

class Person(NamedTuple):
    name: str
    age: int

test_person = Person("test_person_name", 23)
print(test_person.name)
print(test_person.age)
# test_person.dynamic_instance_variable = 22  # AttributeError: 'Person' object has no attribute 'dynamic_instance_variable'
```

When using ```typing.NamedTuple```, the class variables are used as instance variables.

## Eagerly computed attributes, dataclasses, and ```__post_init__()```

The dataclasses module in Python has the same concept as the lombok library in Java. It offers your class a lot of functionality and you have to do a lot less work, the class will look a lot cleaner and it will be a lot easier to maintain.
The ```@dataclass``` decorator will transform your normal class into a dataclass. You can also give arguments to the decorator ( you can give it the ```frozen=true``` argument in order to create a frozne class ). The ```@dataclass``` decorator generates an a lot of methods for you, like ```__init__()``` and ```__repr__()```.
The ```__post_init__()``` method is called after the ```__init__()``` method.

In a dataclass, the ```__init__()``` method is generated for you by using the class attributes. 

```Python
@dataclass()
class RateTimeDistance:
    rate: Optional[float] = None
    time: Optional[float] = None
    distance: Optional[float] = None

    def __post_init__(self) -> None:
        print("POST INIT")
        if self.rate is not None and self.time is not None:
            self.distance = self.rate * self.time
        elif self.rate is not None and self.distance is not None:
            self.time = self.distance / self.rate
        elif self.time is not None and self.distance is not None:
            self.rate = self.distance / self.time


if __name__ == '__main__':
    r1 = RateTimeDistance(time=1, rate=0)
    print(r1.distance)
```

You only have to give 2 instance attributes to this class, the other attribute will be eagerly computed in the ``__post_init__()``` method.

## Incremental computation with ```__setattr__()```

> We can create classes which use ```__setattr__()``` to detect changes in attribute values. This can lead to incremental computation. The idea is to build derived values after initial attribute values have been set.

You can use the ```__setattr__()``` method in order to implement incremental computation. If you change the value of a certain attribute inside your class, other attributes will change to, automatically.

Example:

```Python
class RTD_Dynamic:
    def __init__(self) -> None:
        self.rate: float
        self.time: float
        self.distance: float

        super().__setattr__('rate', None)
        super().__setattr__('time', None)
        super().__setattr__('distance', None)

    def __setattr__(self, name: str, value: float) -> None:
        if name == "rate":
            super().__setattr__('rate', value)
        elif name == "time":
            super().__setattr__("time", value)
        elif name == "distance":
            super().__setattr__("distance", value)
            
        if self.rate and self.time:
            super().__setattr__("distance", self.rate * self.time)
        elif self.rate and self.distance:
            super().__setattr__("time", self.distance / self.rate)
        elif self.time and self.distance:
            super().__setattr__("rate", self.distance / self.time)
```

## The ```__getattribute__()``` method

The ```__getattribute__()``` method is called whenever you are calling an attribute from the class, wether known or unknown.
The default implementation of this method will try to return the value from the ```__dict__``` or ```__slots__``` attributes of the class. If the attribute is now found, the method calls ```__getattr__()``` as a fallback.

Here are some things that we can implement by overriding this method:

* We can effectively prevent access to attributes. This method, by raising an exceptio oinstaed of returning a value, can make an attribute more secret than if we were to merely use the leading underscore (```_```) to mark a name as private to the implementation
* We can invent new attributes similarly to how ```__geattr__()``` can invent new attributes. In this case, however, we can bypass the default lookup done by the default version of ```__getattribute__()```.

Example of the first implementation:

```Python
class SuperSecret:
    def __init__(self, hidden: Any, exposed: Any) -> None:
        self._hidden = hidden
        self.exposed = exposed

    def __getattribute__(self, item: str):
        if (len(item) >= 2 and item[0] == "_") and item[1] != "_":
            raise AttributeError(item)

        return super().__getattribute__(item)
```

## Descriptors

A descriptor is a class that mediates attribute access. The descriptor class can be used to get, set or delete attribute values. They are built at class definition time.
There are 2 types of descriptors:

* A non-data descriptor is a read-only descriptor that only allows you to get the data from inside of it, but it doesn't allow you to change it. This type of descriptor only implements the ```__get__()``` method.
* A data descriptor is a descriptor that allows you to change the value that is inside of it. This type of descriptor implements the ```__get__()``` method and at least one of the two ```__set__()``` and ```__delete__()``` methods.

Here is an example of a data descriptor:

```Python
class LoggedAccess:
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = "_{0}".format(name)

    def __get__(self, obj, objtype):
        value = getattr(obj, self.private_name)
        logging.info("Accessing {0} giving {1}".format(
            self.public_name,
            value
        ))
        return value

    def __set__(self, obj, value) -> None:
        logging.info("Updating {0} to {1}".format(
            self.public_name,
            value
        ))
        setattr(obj, self.private_name, value)


class Person:
    name = LoggedAccess()  # First descriptor instance
    age = LoggedAccess()  # Second descriptor instance

    def __init__(self, name: str, age: int) -> None:
        self.name = name  # Calls the first descriptor
        self.age = age  # Calls the second descriptor

    def birthday(self) -> None:
        self.age += 1
```

**Descriptors can only be implemented using class attributes**. 
You can think of a descriptor as an external getter/setter for a value.

## Attribute Design Patterns

In Python, it's common to treat all attributes as public. This mean the following:

* All attributes should be well documented.
* Attributes should properly reflect the state of the object; they shouldn't be temporary or trasient values.
* In the rare case of an attribute that has a potentially confusing ( or brittle ) value, a single leading underscore character (```_```) marks the name as *not part of the defined interface*. It's not techincally private, but it can't be relied on in the next releasee of the framework or package.

It's important to think of private attributes as a nuisance. Encapsulation isn't broken by the lack of compelx privacy mechanisms in the language; propert encapsulatin canonly be broken by bad design.
Additionally, we have to choose between an attribute or a rpoperty which has the same syntax as an attribute, but can have more complex semantics.

# 5. The ABCs of Consistent Design

## Abstract base classes

An abstract base class has the following features:

* Abstract means that these classes don't contain all the method definitinos required to work completely. For it to be a usefull subclass, we will need to provide some method definitions.
* Base means that the other classes will use it as a superclass. Abstract base classes are not made to be instantiated.
* An abstract class provides some definitions for methods. Most importantly, the abstract base classes often provide the signatures for the missing methods. A subclass must provide the right methods to create a concrete class that fits the interfae define by the abstract class.

You can create an abstract base class that is also a container by using the ```collections.abc``` module:

```Python
import collections.abc

class SomeApplicationClass(collections.abc.Sequence):
    pass
```

Now that the *SomeApplicationClass* was defined as a ```Sequence```, it will have to implement the specific methods required by the ```Sequence``` abstract base class.

## Base classes and polymorphism

> In this section, we'll get into the idea of **pretty poor polymorphism. Inspection of argument value types is a Python programming practice that should be isolated to a few special cases. Later, when we look at numbers and numeric coercion, we'll learn about cases where the inspection of types is recommended.
> Well-done polymorphism follows what is sometimes claled the **Liksov substituion principle**. Polymorphic classes can be used intercahngeably. Each polymorphic class has the same suite of properties. 
> Overusing ```isinstance()``` to distinguish between the types of arguments can lead to a needlessly compelx ( and slow ) program. Unit testing is a far better way to find programming errors than verbose type inspection in the code.
> Method functions with lots of ```isinstance()``` methods can be a symptomp of a poor ( or incomplete ) design of polymorphic classes. Rather than having type-specific processing outside of a class definition, it's often better to extend or wrap classes to make them more properly polymorphic and encapsulat the type-specific processing withint the class definition.

> The python approach is summarized as follows:
> *"It's better to ask for forgiveness than to ask for permission."*
> This is generally taken to mean that we should minimize the upfront testing of arguments ( asking permission ) to see if they're the correct type. Argument-type inspections are rarely of any tangible benefit. Instead we should handle the exceptions appropriately ( asking forgiveness ).
> Checking types in advance is often called **look before you leap (LBYL)** programming. It's an overhead of relatively little value. The alternative is called **easiert to ask for forgiveness than permission (EAFP)** programming, and relies on ```try``` statements to recover from problems.

## Callable

Python's definition of *callable** objects includes the function definitions using the ```def``` statement.

The ```Callable``` type hint is used to describe an object that contains the dunder call method ( ```__call__``` ).

## Containers and collections

When creating a new kind of container, we have 2 general approaches:

* We can use the ```collections.abc``` module to build new containers and formally inherit behavior from the abstract base classes.
* We can rely on type hinting to confirm that methods match the needed protocol.

The formality of using ```collections.abc``` has the following advantages:

* It advertises what our intentino was to people reading our code. When we are making a subclass that inherit from a class from the ```collections.abc``` module, we are making a very strong claim about the functionality of that class and how it should be used.
* It creates some diagnostic support. If we fail to implement all of the required methods properly, an exception will be raised when trying to create instances of the abstract base class.

## MRO and metaclasses

Classes in python can be seen as objects ( read https://realpython.com/python-metaclasses/ ). They are built using ```type```. ```type``` is also a metaclass and inherits from itself. 
The MRO ( method resolution order ) returns a tuple with all the bases of a class, in order.

## The abc and typing modules

The ```ABCMeta``` class is a metaclass that ensure that abstract classes can't be instantiated and that subclasses must implement all the abstract methods ( use ```@abstractmethod``` for that ) in order to be allowed to build instances.

## Using the ```__subclasshook__()``` method

> We can define absract base classes with complex rules for overrides to create concrete subclasses. This is done by implementing the ```__subclasshook__()``` method of the abstract base class.

## Abstract classes using type hints

You can also use type hinting in order to check for abstract classes. Example:

```Python
from typing import Tuple, Iterator, Any


class LikeAbstract:
    def aMethod(self, arg: int) -> int:
        raise NotImplementedError


class LikeConcrete(LikeAbstract):
    def aMethod(self, arg1: str, arg2: Tuple[int, int]) -> Iterator[Any]:
        pass
```

The concrete class will be checked by mypy to be sure that it matches the type hints from the abstract method. It's not as strict as the checks that are made by the ```ABCMeta``` class.

## Short summary

A rule for good class design is to inherit as much as possible. 
There are three fundamental design strategies when it comes to containers:

* Wrapping an existing container
* Extending an existing container
* Inventing a wholly new kind of container

Most of the time we will use the first two strategies; wrapping an existing container or extending an existing container. This fits with the rule of inheriting as much as possible.


# 6. Using Callable and Contexts

The concept **callable** in Python enables us to create functions and classes that behave like functions.
We can create for example a **callable** object that uses *memoization* to cache answers in order to make an algorithm faster.

The concept of **context** allows u to create reliable resource management. The ```with``` statement defines the start of a context and creates a context manager to control resources used in that context. 
We can add certain actions that happen automatically at the start/end of a context. This allows us to safely open/exit files or to separate cross-cutting concerns in certain cases. When opening files in a context manager, python returns by default a context manager that safely closes files for you.

## Callables

### Example of a callable

There are 2 ways of designing callables in Python:

* By creating a normal function using the ```def``` statement.
* By creating an instance of a class that implements the ```__call__()``` method. You can signal that a class is meant to be a callable class by using ```collections.abc.Callable``` as its base class.

Example of a callable class:

```Python
from typing import Callable, Dict

IntExp = Callable[[int, int], int]


class Power:
    def __init__(self, a: str):
        self.a = a

    def __call__(self, x: int, n: int) -> int:
        p = 1
        for i in range(n):
            p *= x

        return p



if __name__ == "__main__":
    pow: IntExp = Power4()
    print(pow(2, 1024))
```

### Abstract base class for callables

You can see that we are calling the class, just like we would call any other normal function. The problem with this class is that, if it would get a lot longer, it wouldn't be clear that this is meant to be used as a *callable*. On top of that, if we would have any problem with the ```__call__()``` method, it would be a lot easier to debug it if we would inherit this class from a abstract base class.
In order to fix this problem we have to make the class inherit from ```collections.abc.Callable```:

```Python
import collections.abc
from typing import Callable, Dict

IntExp = Callable[[int, int], int]


class Power(collections.abc.Callable):
    def __init__(self, a: str):
        self.a = a

    def __call__(self, x: int, n: int) -> int:
        p = 1
        for i in range(n):
            p *= x

        return p



if __name__ == "__main__":
    pow: IntExp = Power4()
    print(pow(2, 1024))
```

### Callables with memoization

The idea of memoization is to cache (save) certain results of a predicate based on a certain number of steps that have been taken to get to the result, when the predicate is called again using the exact same sequence of steps, rather than computing the result again, we are returning the cached result.

We can speed up the process of computing by using memoization. The trade-off of memoization is memory. The algorithm will use a lot less CPU power and will be a lot faster but it will use a lot more memory since it has to store the cached values.

Example of a callable with memoization:


```Python
class Power(collections.abc.Callable):
    def __init__(self) -> None:
        self.memo: Dict = {}

    def __call__(self, x: int, n: int) -> int:
        if (x, n) not in self.memo:
            if n == 0:
                self.memo[x, n] = 1
            elif n % 2 == 1:
                self.memo[x, n] = self.__call__(x, n - 1) * x
            elif n % 2 == 0:
                self.memo[x, n] = self.__call__(x, n // 2)
            else:
                raise Exception("Logic Error")

        return self.memo[x, n]
```

The cached values are stored inside the ```self.memo``` dictionary and returned every time the same arguments are given to the callable.

### Functools memoization

The ```functools``` library contains a bunch of helpful tools for functions/callables/classes etc.
Probably one of the most used decorator from the ```functools``` library is ```lru_cache```. 
The ```lru_cache``` decorator implements memoization in your function:

Example:

```Python
from functools import lru_cache


@lru_cache()
def pow(x: int, n: int) -> int:
    if n == 0:
        return 1
    elif n % 2 == 1:
        return pow6(x, n - 1) * x
    else:
        t = pow6(x, n // 2)
        return t * t
```

## Managing contexts and the ```with``` statement

When you open a file using the ```with``` statement, a context manager is created around that process. After you do your work, the context manager will automatically close the file for you.

> When the ```with``` statements end, the contexts exit and the files are properly closed; this means that all the buffers are flushed an the operating system resources are released. Even if there's an exception in the body of the ```with``` context, the context manager's exit will be processed correctly and the file will be closed.

> **Always use a with statement around a path.open() and related file-system operations

> Since files involve operating system resources, it's important to be sure that the entanglements between our appliation and the OS are released as soon as they're no longer needed. The ```with``` statement ensures that resources are used properly.

### Defining the ```__enter__()``` and ```__exit__()``` methods

When building a custom context manager, it has two special methods: ```__enter__()``` and ```__exit__()```. These are used by the context manager when it starts/ends.

> We'll often use context managers to make global state changes. This might be a change to the database transaction status or a change to the locking status of a resource, something that we want to do and then undo when the transaction is complete

Example of a simple custom context manager:

```Python
from typing import Optional, Type
from types import TracebackType


class CustomContextManager:
    def __enter__(self) -> None:
        print("enter")

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType]
    ) -> None:
        print("exit")

with CustomContextManager():
    print("Inside the custom context manager")

"""
Output:
enter
Inside the custom context manager
exit
"""
```

You can also handle exception directly from the ```__exit__()``` method. If the context manager exists with a certain error, you can program it to do something automatically for that certain case.

### Context manager as a factory

We can use the context manager as a factory as well. We can use the special method enter ( ```__enter__()``` ).

### Context manager design considerations and trade-offs

> A context is generally used for acquire/release, open/closed and lock/unlock types of operation paris. Most of the examples are file I/O related, and most of the file-like objects in Python are already proper context managers.

> A Context manager is almost always required for anything that has steps that bracket the essential processing. In particular, anything that requires a final ```close()``` method should be wrapped by a context manager.

# 7. Creating Containers and Collections

**Documentation to the python data model: https://docs.python.org/3/reference/datamodel.html**

There are a lot of options when it comes to containers and collections. We can either use the built-in containers ( lists, sets, dictionaries, etc. ) or we can use the collections library which includes things like deques, ChainMaps, etc.
We also have the option to create our own containers by using the **abstract base classes** which also provides us with design guidelines and gives the users a general idea of what our new container is supposed to be used for and under what circumstances. However, it is very rare that you are going to need a new type of container.

## ABCs of collections

### Basics of ABCs and polymorphism

The ```collections.abc``` module gives us the ability to decompose self-made collections into smaller sets in order to describe their functionality. **A related set of features of a class is called a *protocol***.
An example of a protocol is for example the ability to get, set and delete items which would describe the protocol for list-like behavior. So is the ```__iter__()``` method part of the protocol for defining an iterable container. A fully functioning list might/should implement both of these protocols. You should be able to add, get and delete items as well as iterate over them.

We usually tend to use a ```list``` without thinking about the underlining features than lay behind it and how it deeply relates to other data structures like ```sets``` or even ```dicts```. Once we look at the ABCs of these data structures we can see how they relate to each other and how they are the same in many aspects. They all have numerous protocols in common. At the core of all these collections we can find the core protocols.

> By decomposing the aspects of each collection, we can see areas of overlap that manifest themselves as an elegant polymorphism, even among different data structures.

### Single Method Base Classes and Composite Base Classes

Let's take a look at the following base classes that only define a single method ( these are part of the core protocols that containers can implement ):

* The ```Container``` ABC requires the concrete class to implement the ```__contains__()``` method. This special method implements the ```in``` operator.
* The ```Iterable``` ABC requires the concrete class to implement the ```__iter__()``` method. This special method is used by the ```for``` statement as well as generator expressions and the ```iter()``` function.
* The ```Sized``` ABC requires the concrete class to implement tthe ```__len__()``` method. This method is used by the ```len()``` function.
* The ```Hashable``` ABC requires the concrete class to implement the ```__hash__()``` method. This is used bby the ```hash()``` function. **If this method is implement, that means that the object is immutable**.

All of these ABCs are used to build higher-level composite definitions of structures that we can use. These composite structures include lower-level ABCs.
Here are some composite ABCs that we could implement:

* The ```Sequence``` and ```MutableSequence``` ABCs are built from the basic ABCs and implement methods such as ```index()```, ```count()```, ```reverse()```, ```extend()``` and ```remove()```.
* The ```Mapping``` and ```MutableMapping``` classes contain methods such as ```keys()```, ```items()```, ```values()``` and ```get()```.
* The ```Set``` and ```MutableSet``` classes include comparison and arithmetic operators to perform set operations.

## Examples of special methods

If you find yourself in the situation where you have to repeat a certain task that could easily be packed in a special method, it might be better to override the special method.

Let's look at an example where your collection is based on the concept of wrapping a collection and delegating methods to it. Example:

```Python
class A:
    def __init__(self) -> None:
        self.my_collection: List[Any] = list()
    def append(self, *args: List[Any]) -> None:
        self.my_sequence.extend(args)
```

Now, let's say that you need to check if you can find a certain number in the wrapped collection multiple times.

You can use ```any```:

```Python
a_instance = A()
a_instance.append(1, 2, 3, 4, 5)
search_number = 2
any(item == search_number for item in a_instance) # True
```

If you have to implement this ```any``` method multiple times, you might be better of, overriding the ```__contains__``` special method:

```Python
class A:
    def __init__(self) -> None:
        self.my_collection: List[Any] = list()
    def append(self, *args: List[Any]) -> None:
        self.my_sequence.extend(args)
    def __contains__(self, search_number: int) -> bool:
        return any(item == search_number for item in self.my_collection)

my_instance = A()
my_instance.append(1, 2, 3, 4, 5)
print(1 in my_instance) # True
print(2 in my_instance) # True
print(3 in my_instance) # True
print(4 in my_instance) # True
print(5 in my_instance) # True
print(6 in my_instance) # False
```

You can see that from a design point of view, it looks a lot easier and it's a lot more practical.

## Standard Library Extensions

The standard library offers extensions to built-in classes. Some examples are ```deque```, ```ChainMap```, ```defaultdict```, ```Counter```.

There are two collections that have been replaced by more advanced versions:

* The ```namedtuple()``` collection has been replaced by the ```typing.NamedTuple``` class because it permits type hints.
* The ```OrderedDict``` collection is not needed anymore, you can use the built-in ```dict``` collection since the feature of maintaining key order is now a first-class part of the built-in class ```dict``` is the special collection ```OrderedDict``` is not necessary anymore.

### The ```typing.NamedTuple``` class

The ```typing.NamedTuple``` class requires class attributes. These attributes will usually have type hints and provide a way to give names to attributes of the tuple.

> Using a ```NamedTuple``` subclass can condense a class definition into a very short definition of a simple immutable object. It saves us from having to write longer and more complex class definitions for the common case where we want to name a fixed set of attributes.

Example:

```Python
from typing import NamedTuple, List, str

class Student(NamedTuple):
    class_name: str
    name: str
    age: int
    address: str
    classes: List[str]
```

I won't go over the other collections in the standard library since they're trivial.

## Creating new kinds of collections

### The 4 step process to new collections

When it comes to creating new types of collections you must follow the following process that contains of 4 steps:  

1. Define the requirements. This may include research on data structures.
2. Look at the ```collections.abc``` module to see what methods must be implemented to create the new functionality.
3. Create test cases for the new data structure.
4. Write code based on the previous research steps.

The importance of researching the fundamentals has to be emphasized. See any of the following books:

* *Introduction to Algorithms* by Cormen, Leiserson, Rivest and Stein
* *Data Structures and Algorithms* by Aho, Ulmna and Hopcroft
* *The Algorithm Design Manual* by Steven Skiena

### ABCs kinds of collections and design strategies

The ABCs defines three broad kinds of collections: sequences, mappings and sets.
There are three design strategies that we can use to create new kinds of collections:

* **Extend**: Extend an already existing collection
* **Wrap**: Wrap an existing collection
* **Invent**: Invent a new type of collection that is built from scratch

Another design consideration would be choosing between eager and lazy calculation when it comes to certain values.

### Narrowing a collection's type

When it comes to type hinting python allows us to provide extensive type hints to our collections. This has the following advantages:

* It helps us visualize the data structures
* It helps running **mypy** to confirm that the code uses the data structure properly

We already know about the basic type hints for non-collection types ( ```int```, ```float```, ```str```, ```complex```, etc. ) but you can also build type hints from the ```typing``` module for collections. You will probably often see ```from typing import List, Tuple, Dict, Set```

Each of those type hints offers even more parameters and complexity in order to allow you to further narrow a collection's type:

* The ```List[T]``` argument allows a list to only contain items of the type ```T```. A list of ```[1, 2, 3, 4, 5]``` can be described as a list of integers, so it's a ```List[int]```. Same principle goes for ```Set[T]``` for example.
* The ```Dict[K, V]``` requires the object to be a dictionary and to contain key-value pairs of the type ```K``` ( for keys ) and ```V``` ( for values ). For example the dictionary ```{'a': 1, 'b': 2}``` might be described as a dictionary that contains key-value pairs of the type ```str``` and ```int```, so it would be ```Dict[str, int]```.

The ```Tuple``` hint is more complex. There are two common cases for tuples:

* A hint that looks for example like this: ```Tuple[str, int, int, int]``` only allows you to have a Tuple that contains 4 values of those exact types, for example: ```('string', 1, 2, 3)```. The size of the tuple and the order of the elements is crucial.
* A hint such as ```Tuple[int, ...]``` describes a tuple of indefinite size that only contains items of type ```int```. The size is not specified.

In order to describe values that might pe ```None```, the type hint ```Optional``` is used. If we want a list that contains a mixture of ```int``` and ```None``` values, we would use ```List[Optional[int]]```.

### Working with ```__getitem__()```, ```__setitem__()```, ```__delitem__()``` and slices


Sequences have two different kinds of indexes:

* ```a[i]```. This is a simple integer index
* ```a[i:j]``` or ```a[i:j:k]```. These are ```slice``` expressions with ```start:stop:step``` values. Slice expressions can be quite compelx, with seven different variations for different kinds of values.

The basic syntax works in three contexts:

* In an expression, relying on ```__getitem__()``` to get a value
* On the left-hand side of assignment, relying on ```__setitem__()``` to set a value
* On a ```del``` statement, relying on ```__delitem__()``` to delete a value

When we do something like ```seq[:-1]```, we write a ```slice``` expression. The underlying ```__getitem__()``` method will be given a ```slice``` object, instead of a simple integer.

The reference manual tells us a few things about slices. A ```slice``` object will have three attributes: ```start```, ```stop``` and ```step```. It will also have a method function called ```indices()```, which will properly compute any omitted attribute values for a slice.

So basically:

```a = some_list[1]``` is when you access something from the list, so you want to get a value/an item. In this situation we call ```__getitem__(self, key)```. The key is in our example ```1```. The key can be an index or a ```slice``` object. A slice object contains 3 attributes: ```start```, ```stop``` and ```step``` and is called when we have something like ```a = some_list[1:2:3]```. In this case, the ```start``` is 1, ```stop``` is 2 and ```step``` is 3.

If you want to set a specific item from the collection using ```collection[index] = new_value```, you will use ```__setitem__(self, key, value)``` where the ```key``` is the index and the ```value``` is the new value of the item at that ```key```.

If you use the delete (```del```) statement : ```del collection[index]```, you will use the ```__delitem__(self, key)``` dunder method where the ```key``` is the index of the item that must be deleted.

Here is a short example:

```Python
from typing import Any

class TestContainer():
    def __init__(self, *items: Any):
        self.internal_list = [] if items is None else list(items)

    def __setitem__(self, index: int, value: Any) -> None:
        print("Execute __setitem__ with --> index : {0} && value : {1}".format(index, value))
        self.internal_list[index] = value

    def __delitem__(self, index: int) -> None:
        print("Execute __delitem__ with -- > index : {0}".format(index))
        del self.internal_list[index]

    def __getitem__(self, key: Any) -> None:
        print("Execute __getitem__ with -- > key : {0}".format(key))
        return self.internal_list[key]

    def __str__(self )-> str:
        return str(self.internal_list)
```

## Wrapping a list and delegating

We'll now look at how we can wrap a built-in container in a made up collection. There is a substantial amount of code that comes in play when we have to wrap a container since we have to delegate a considerable amount of methods to it. 
This is useful when we want to restrict certain methods for example. A common restriction that applies to statistics data classes is that thye need to be *insert only* which means that our built-in list container is perfectly fine, it just needs to have some methods restricted from the outside. There are of course other usefull application where we can apply this design of wrapping built-in containers. In our example with the statistical data, we'll be disabling a number of method functions. This is the kind of dramatic change in the class features that suggests using a wrapper class instead of an extension.

### Creating iterators with ```__iter__()```

When our design involves wrapping an exisitng container we have to make sure that our class is iterable. We can of coures again look at the ABCs for containers and see that there is a class called ```collections.abc.Iterable```. When using that ABC class we will only need to implement one single dunder method, that being ```__iter__()``` in order to make an object iterable. **The ```__iter__()``` method can either retrun a proper ```Iterator``` object, or it can be a generator function.**

> Creating an ```Iterator``` object, while not terribly complex, is rarely necessary. It's much simpler to create generator functions. For a wrapped collection, we should always simply delegate the ```__iter__()``` method to the underlying collection.

Example:

```Python
from typing import Any
import collections.abc

class TestContainer(collections.abc.Iterable):
    def __init__(self, *items: Any):
        self.container = [] if items is None else list(items)

    def __iter__(self):
        return iter(self.container)

container = TestContainer(1, 2, 3, 4, 5)

# Iterator over the container object and print : 1 2 3 4 5
for i in container:
    print(i)
```

## Creating a new kind of set/container

> Creating a whole new collection requires some preliminary work. We need to have new algorithms or new internal data structures that offer significant improvements over the built-in collections. It's important to do thorough Big-O complexity calculations before designing a new collection. It's also important to use ```timeit``` after an implementation to be sure that the new collection really is an improvement over available built-in classes.

## Design considerations and tradeoffs

When working with containers and collections we have a multistep design strategy:

1. Consider the built-in versions of sequence, mapping and set.
2. Consider the library extensions in the collection module, as well as extras such as ```heapq```, ```bisect``` and ```array```.
3. Consider a composition of existing class definitions. In many cases, a list of ``tuple``` objects or a ```dict``` of lists provides the needed features.
4. Consider extending one of the earlier mentioned classes to provide additional methods or attributes.
5. Consider wrapping an existing structures as another way to provide additional methods or attributes.
6. Finally, consider a novel data structure. Generally, there is a lot of careful analysis avaiable. Start with Wikipedia articles such as this one: https://en.wikipedia.org/wiki/List_of_data_structures.

Once the design alternatives have been identified, there are two parts of the evalution left:

* How well the interface fits with the problem domain. This is a relatively subjective determination.
* How well the data structure performs as measured with ```timeit```. This is an entirely objective result.

It's important to avoid the paralysis of analysis. We need to *effectively* find the proper colleciton.

In most cases, it is best to profile a working application to see which data structure is the performance bottleneck. In some cxases, consideration of the complexity factors for a data structure will reveal its suitability for a particular kind of problem before starting the implementation.

**Perhaps the most important consideration is this: for the highest performance, avoid search**.

Avoiding search is the reason sets and mappings reuqire hashable objects. A hashable objectx can be located in a set or mapping with almost no processing. Locating an item by value ( not by index ) in a list can take a great deal of time.

# 8. Creating Numbers

We can extend the ABC abstractions in the ```numbers``` (https://docs.python.org/3/library/numbers.html) module to create new kinds of numbers. We can do this in order to create numbers that fit our problem domain more precisely. The abstractions in the ```numbers``` module need to be looked at first, because they define the existing built-in classes. Before working with new kinds of numbers, it's essential to see how the existing numbers work.

## Deciding which types to use

There are four general domains of numerical processing:

* **Complex**: This domain is used once we get involved in complex math. We will use ```complex```, ```float``` and the ```cmath``` module.
* **Currency**: For currency-related operations we must use ```Decimal```. When we do currency-related operations it's generally a bad idea to mix ```decimal``` values with non-decimal values. We can't use ```float``` either since ```float``` values are approximations and that is absolutely unacceptable when working with currency.
* **Bit Kicking**: For operations that involve bit and byte processing, we'll generally only use ```int```.
* **Conventional**: This is a broad category where *everything else* can be put in.

> These are generally obvious aspects of a given problem domain. It's often easy to distinguish applications that might involve science or engineering and complex numbers from applications that involve financial calculations, currency, and decimal numbers. It's important to be as permissive as posisble in the numeric types that are used in an application. **Needlessly narrowing the domain of types via the ```isinstance()``` test is often a waste of time and code.**

## Method resolution and the refelcted operator concept

The arithmetic operators ( +, -, *, / ,//, %, **, etc. ) are all mapped to special methods. When we write ```1+2``` for example, what actually happens behind the scenes, is, python takes the left-most operand and execute the method that is mapped to the arithemtic operator on the right-most operand. So ```1+2``` would be ```1.__add__(2)``` since the ```+``` operator maps to the ```__add__()``` special method. The simplest rule is that the left-most operand determines the class of the operator being used.

There are however cases where we do this differently. Let's take a look at the following example:

If you have the following expression: ```2 - 0.5``` you might think that we will take the most operand and apply the dunder method that maps to the ```-``` arithmetic operation, which would be ```__sub__()```, so we would have ```2.__sub__(0.5)```. This is however wrong. As you can see we have 2 numbers of different types. One number is an integer and the other number is a float. If we would use the integer to be the leader of the operation, we would lose precision since integers are more general than float numbers. **Converting up the tower of types ( from ```int``` toward ```complex``` ) won't lose precision. Converting down the tower of types implies a potential loss of precision.**
In this example, we will use the right-hand side operand since we won't lose any precision that way. We won't use the ```__sub__()``` method since that is for left-side operands, we will have to use the ```__rsub__()``` method. So, in our case ```2-0.5``` would be ```0.5.__rsub__(2)```.

The ```__rsub__()``` operation is called **reflected subtraction**. The ```a.__sub__(b)``` operation is the expected subtraction while the ```b.__rsub__(a)``` is the reflected subtraction; the implementation method in the latter comes from the right-hand side operand's class. So far, we've seen the following two rules:

1. Rule one: try the left-hand side operand's class first. If that works, good. If the operan return ```NotImplemented``` as a value, then use rule two.
2. Rule two: try the right-hand side operand with the reflected operator. If that works, good. If it returns ```NotImplemented```, then it really is not implemented, so an exception must be raised.

The notable exception is when the two operands happend to have a subclass relationship.

The following additional rule applies before the first pair rules as a special one:

* If the right operand is a subclass of the left, and the subclass defines the reflected special method name for the operator, then the subclass reflected operator will be tried. This allows a subclass override to be used, even if the subclass operand is on the right-hand side of the operator.
* Otherwise, use rule one and try the left side.

## The arithmetic operators special methods.

|Method|Operator|
|------|--------|
|```object.__add__(self, other)```|+|
|```object.__sub__(self, other)```|-|
|```object.__mul__(self, other)```|*|
|```object.__truediv__(self, other)```|/|
|```object.__flooridv__(self, other)```|//|
|```object.__mod__(self, other)```|%|
|```object.__divmod__(self, other)```|divmod()|
|```object.__pow__(self, other[, modulo])```|pow() as well as **```**```**|

Remember that for every expected operation, there is also a reflected one. ( Example: ```__rsub__()``` ).

> A unary operation is an operation with only one operand. As unary operations have only one operand, they are evaluated before other operations containing them.Common unary operators include Positive (+) and Negative (-).
> Unary positive also known as plus and unary negative also known as minus are unique operators. The plus and minus when used with a constant value represent the concept that the values are either positive or negative. 
(from [source](https://press.rebus.community/programmingfundamentals/chapter/unary-operations/#:~:text=Unary%20positive%20also%20known%20as,are%20either%20positive%20or%20negative))

Here are the unary operators and functions:

### Unary operators and methods


|Method|Operator|
|------|--------|
|```object.__neg__(self, other)```|-|
|```object.__pos__(self, other)```|+|
|```object.__abs__(self, other)```|abs()|
|```object.__complex__(self, other)```|complex()|
|```object.__int__(self, other)```|int()|
|```object.__float__(self, other)```|float()|
|```object.__round__(self, other[, n])```|round()|
|```object.__trunc__(self, other[, n])```|math.trunc()|
|```object.__ceil__(self, other[, n])```|math.ceil()|
|```object.__floor__(self, other[, n])```|math.floor()|

### Comparison operators and methods

|Method|Operator|
|------|--------|
|```object.__lt__(self, other)```|<|
|```object.__le__(self, other)```|<=|
|```object.__eq__(self, other)```|==|
|```object.__ne__(self, other)```|!=|
|```object.__gt__(self, other)```|>|
|```object.__ge__(self, other)```|>=|

### Bitwise operators and methods

|Method|Operator|
|------|--------|
|```object.__lshift__(self, other)```|<<|
|```object.__rshift__(self, other)```|>>|
|```object.__and__(self, other)```|&|
|```object.__xor__(self, other)```|^|
|```object.__or__(self, other)```|```|```|
|```object.__invert__(self)```|~|

### In-place operators and methods

|Method|Operator|
|------|--------|
|```object.__iadd__(self, other)```|+=|
|```object.__isub__(self, other)```|-=|
|```object.__imul__(self, other)```|*=|
|```object.__itruediv__(self, other)```|/=|
|```object.__ifloordiv__(self, other)```|//=|
|```object.__imod__(self, other)```|%=|
|```object.__ipow__(self, other[, modulo])```|**=|
|```object.__ilshift__(self, other)```|<<=|
|```object.__irshift__(self, other)```|>>=|
|```object.__iand__(self, other)```|&=|
|```object.__ixor__(self, other)```|^=|
|```object.__ior__(self, other)```|```|=```|

# 9. Decorators and Mixins - Cross-Cutting Aspects

Cross-Cutting concerns represent aspects of our application that cut through the implementation of multiple structures. Such concerns might be for example logging, security or even transaction management. One way of reusing functionality in OOP is to use inheritance. However, inheritance doesn't always work out well. 

A decorator provides a way of defining functionality that is not bound to the inheritance hierarchy. We can use decorator in order to define an certain aspects of our application and then spread them around our application withG$ classes, methods or functions.

Another way of dealing with cross-cutting concerns would be multiple inheritance.

> It's important to note that corss-cutting concerns are rarely specific to the application at hand. They're often generic considerations. The common examples of logging, auditing, and security could be considered as infrastructure separate from the application's details.

## Class and meaning

Objects can be classified. Every object belongs to a certain class. This leads to a straightforward relationship between object and class. However, this is only the case when we are looking at single-inheritance design.

When we involve multiple-inheritance, the classification problem can become more complex since a class can now inherit from multiple classes. When we look for example at a coffe cup, we can clearly see that it is a container. But we don't only look at it as a simple container. There are more attributes that it can have, other than just how much liquid it can contain. When we look at a coffe cup we see multiple things. We can see a container, a certain type of material, certain paintings, shape, glaze, etc. A cup of coffe is not just a simple container, it inherits multiple attributes from different kinds of classes.

Most objects have a simple straightforward ***```is-a```** with a class. In our coffe-cup problem domain, the coffe cup won't be able to have a straightforward is-a relationship with the container class, since a coffe-cup is so much more than a container.

> Generally, these other features can be seen as mixin classes, and they define the additional interfaces or behaviors for an object. The mixing classes may have their own hierarchies, for example, ceramic art is a specizliation of the mroe general sculpture and art classes.

> When doing object-oriented design in Python, it's helpful to identify the ```is-a``` class and the essential aspects define by that class. Other classes provide ```acts-as``` aspects, which mix in additional interfaces or behavior for an object.



## Type hints and attributes for decorators

There are 2 stages when it comes to building decorators. The first stage is creating a function and the second stage involves the application of the decorator.

When we apply a decorator (```@decorator```) to a function ```F```, it is as if we've created a new function ```F'``` that is equal to ```F'=@decorator(F)```. The name of the function stays the same, but it's functionality will be different.

This is an example of applying a decorator to a function:

```Python
@decorate
def function():
    pass
```

***This is the same as writing:***

```Python
def function();
    pass

function decorate(function)
```

> The decorator modifies the function definition to create a new function. The essential technique here is that a decorator function accepts a function and returns a modified version of that function.

We can also apply multiple decorators and they will all be executed as nested function calls:

```Python
@decorator1
@decorator2
def function():
    pass    
```

***Is the same as writing:***

```Python
def function():
    pass

function = decorator1(decorator2(function))
```

The following is a typical set of type hints required to define a decorator:

```Python
from typing import Any, Callable, TypeVar, cast

FuncType = Callable[..., Any]
F = TypeVar('F', bound=FuncType)

def my_decorator(func:F) -> F:
    ...
```

## Attributes of a function

A decorator can change the attribute of a function. Here is a table with the attributes of a function:

|Name|Description|
|----|-----------|
|```__doc__```|The docstring, or none|
|```__name__```|The original name of the function|
|```__module__```|The name of the module the function was defined in, or none|
|```__qualname```|The function's fully-qualified name, ```__module__.__name__```|
|```__defaults__```|The default argument values, or none if there are no defaults|
|```__kwdefaults__```|The default values for keyword-only parameters|
|```__code__```|The code object representing the compiled function body|
|```__dict__```|A namespaces for the function's attributes|
|```__annotations__```|The annotations of parameters, including '```return```' for the return annotation|
|```__globals__```|The global namespace of the module that the function was define in; this is used to resolve global variable and is read-only|
|```__closure__```|Bindings for the function's free variables or none; it is read-only|

Except for ```__globals__``` and ```__closure__```, a decorator can change any of these attributes.

## MRO

Regardless if we are talking about multiple or single inheritance every object's class defines a ***Method Resolution Order ( MRO )*** .
The MRO is just like the prototype chain in JavaScript. When we are looking for a method, we start at the first class that is in the MRO which always the object's class. Afterwards, we move up the inheritance chain, which is the MRO. Example:

```
class test1(test2, test3, test4):
    ...
```

***The MRO if the class ```test1``` will be : ```(test1, test2, test3, test4, object)```***
In our example the class ```test1``` inherits from 3 classes ( 4 including the ```object``` class which we never see ). 
When we want to access an attribute from an instance of the class test1, we start looking at the first class from the MRO, which is test1 and we can go up the ladder up to the last class, which is the ```object``` class in order to find an attribute.

When you use multiple inheritence it's important to know how to make use the ```super``` keyword.

Here is the documentation for ```super([type[, object-or-type]])```
> Returns a proxy object that delegates method calls to a parent or sibling class of type. This is useful for accessing inherited methods that have been overridden in a class.

> The object-or-type determines the method resolution order to be searched. The search starts from the class right after the type.

> For example, if __mro__ of object-or-type is D -> B -> C -> A -> object and the value of type is B, then super() searches C -> A -> object.

> The __mro__ attribute of the object-or-type lists the method resolution search order used by both getattr() and super(). The attribute is dynamic and can change whenever the inheritance hierarchy is updated.

So basically let's say that your MRO looks like this: ```(Test4, Test3, Test2, Test1)```. If you are in the class ```Test4``` and you want to access the ```Test2``` super class, you will have to use ```super(Test3, self)```. The ```type``` argument specifies after which class you want to start doing your search in the MRO and the ```object-or-type``` argument specifies which MRO to search.

Example with arguments:

```Python
class Test1:
    def __init__(self, a):
        self.a = a
        print("Calling test 1")


class Test2:
    def __init__(self, b):
        self.b = b
        print("Calling test 2")


class Test3:
    def __init__(self, c):
        self.c = c
        print("Calling test 3")


class Test4(Test3, Test2, Test1):
    def __init__(self, a, b, c, d):
        super(Test2, self).__init__(a) # Test 1
        super(Test3, self).__init__(b) # Test 2
        super(Test4, self).__init__(c) # Test 3

        self.d = d
        print("Calling test 4")


test = Test4(1, 2, 3, 4)
print(test.a)
print(test.b)
print(test.c)
print(test.d)
```

## Constructing a decorated class.

The first stage when it comes to decorating classes is of course, building the class definition with it's methods and properties.
The second stage in class construction if s to apply an overall class decorator to a class definition. This is generally made in order to add features. It's more common to add attributes rather than methods. It's very hard to maintain the class if you decide to add methods since the maintainers have to locate the source for a method that was injected by the decorator.

> The features inherited from the superclasses cannot be modified through decorators since they are resolved lazily by method resolution lookup. This leads to some important design considerations. We generally want to introduce methods and attributes through classes and mixing classes. We should limit ourselves to defining new attributes via decorators.

Here is a table of some of the attributes that are built for a class:

|Attribute|Description|
|---------|-----------|
|```__doc__```|The class's documentation string, or none if undefined|
|```__name__```|The class name|
|```__module__```|The module name that the class was defined in|
|```__dict__```|The dictionary containig the class's namespace |
|```__bases__```|A tuple ( possibly empty or a singleton ) containing the base classes, in the order of their occurrence in the base class list; it is used to work out the method resolution order|
|```__class__```|the superclass of this class, often type|

## Some class design principles

When defining a class, we have the following sources of attributes and methods:

* Any decorators applied to the class definition. These are applied to the definition last.
* The body of the class statement.
* Any mixin classes. These definitions tend to override the base class definitions in the method resolution order algorithm.
* The base class. If unspecified, the base class is ```object```, which provides a minimal set of definitions.o

These are presented in order of their visibility. The final changed from a decorator overwrite everything below it, making these changes most visible. The body of the class statement overrides anything inherited from mixing or the base class. The base class it the last place used to resolve names.

We need to be cognizant about how easy it is for software maintainers to see each of these. The ```clas``` statement is the most obvious place for someone to look for the definition of an attribute or methods. The mixins and the base class are somewhat less obvious than the class body. It's helpful to make sure that the base class name clarifies its role and uses terminology that is clearly essential. For exapmle, it helps to name base classes after real-world objects.

The application of the decorator to the class can lead to obscure features. A strong focus on one or a few features helps to clarify what the decorator does. While some aspects of an application can be suitable for generic decorators, the lack of visibility can make them difficult to test, debug, and maintain.

> When writing the ```class``` statement, the mixins are listed first, and the essential superclass is lsited last. This is the search order for name resolution. The last listed class is the class that defines the essential ```is-a``` relationship. The last class on a list defines what a thing **IS**. The previous class names can define what a thing **DOES**. The mixins provide ways to override or extends this base behavior.

## Aspect-oriented programming

Some parts of aspect-oriented programing are implemented through decorators. The idea of aspect oriented programming is to separate cross-cutting concerns from the actual code. Example of cross-cutting concerns as: Logging, Auditability, Security, Transaction Management etc.

The pythonic approach to AOP involves the use of decorators and mixins:

* **Decorators**: Decorators enable you to establish a consistent aspect implementation at one of two simple join points in a function ( start and end ). We can perform the aspect's processing before or after the existing function. We cna't easily locate join points inside the code of a function.
* **Mixins**: Using mixins we can identify a class as being a component of multiple class hierarchies. The mixin classes can be used with the base class to provide functionality for cross-cutting aspects. Generally, mixin classes are considered abstract, since they can't be meaningfully instantiated.

## Using built-in decorators and standard library decorators

We already know some built-in decorators like ```@classmethod```, ```@staticmethod``` and ```@property```. The ```@property``` decorator transforms a method into a descriptor and getter and then you can also use that "method" to built a setter and deleter. The ```@classmethod``` and ```@staticmethod``` decorators are self-explanatory.

The standard library has a lot of decorators. Modules such as ```contextlib```, ```functools```, ```unittest```, ```atextit```, ```importlib``` and ```reprlib``` contain a bunch of decorators.

One very interesting decorator is from the ```functools``` library and that is the ```functools.total_ordering``` decorator which offers missing comparison operators. It leverages ```__eq__()``` and either ```__lt__()```, ```__le__()```, ```__gt__()``` or ```__ge__()``` to create a complete suite of comparisons. 
You don't need to define all comparison operators. It only needs ```__eq__()``` and one of the other four. 

Example:

```Python
import functools

@functools.total_ordering
class Test:
    def __init__(self) -> None:
        ...

    def __lt__(self, other) -> bool:
        ...

    def __eq__(self, other) -> bool:
        ...
```

Every instance that you will make of a class with this kind of structure will contain all comparison operators. Even if the class doesn't implement all the comparison operators, it does contain the ```__eq__()``` operator and one of the 4 other comparison operators, which makes it enough for the decorator ```@functools.total_ordering``` to implement the rest of them.

## Using standard library mixin classes.

When we defines our own collection and implement abstract classes from the ```collections.abc``` abstract base classes collection we're making use of mixins to ensure that cross-cutting aspects of the containers are defined consistently. Even the top level containers ( ```Set```, ```Sequence``` and ```Mapping``` ) are all built from multiple mixins.

The ```Sequence``` ABC inherits for example from ```Sized```, ```Iterable``` and ```Container```.

> The final behavior of the ```list``` class is a composition of aspects from each of the mixins present in its definition. Fundamentally, it's a ```Container``` with numerous protocols added to it.

## Using the enum with mixin classes

The enum library contains the Enum class. The most cmmon use case for this class it o define an enumerated domain of values.

An enumerated type has the following two features:

* **Member names**: The member names are proper Python identifiers for the enumerated values.
* **Member values**: The memeber values can be any Python object

We can combine the enum class with other mixin classes:

```Python
from enum import Enum

class Enums(str, Enum):
    value1 = "test1.test1"
    value2 = "test2.test2"
    value3 = "test3.test3"
    value4 = "test4.test4"
```

The ```Enum``` class is the base class. We have an additional mixin class, that being the ```str``` class. **This class will be available to each memeber**. 

> The order of the definitions is important: **the mixins are listed first; the base class is listed last.**

Because we have mixed in the ```str``` class, we have provided all the methods of the ```str``` class to each of our members. We can now write something like:

```Python
split_value = Enums1.value1.split(".")
```

> This mixin technique allows us to bundle features together to create complex class definitions from separate aspects.

> ***A mixin design is better than copy and paste among several related classes***

> It can be difficult to create classes that are generic enough to be used as mixins. One approach is to look for duplicated copypast code across multiple classes. The presence of duplicated code is an indication of a possible mixin to refactor and eliminate the duplication.

## Writing a simple function decorator

A ```decorator``` function is a function ( or a callable object ) that takes in a function as a parameter and returns a new function. The result of the decorations is a function that has been wrapped up.

> Generally, the additional features of the wrapping surround the original functionality, either by transforming actual argument values or by transforming the reuslt value. These are the two readily available join points in a function.

When we build a decorator we want to make sure that the decorated/wrapped up function keeps its name and its ```docstring```. These details can be handled for us by a decorator to build our decorators. Using ```functools.wraps``` to write new decorators helps us ensure that the wrapped up function doesn't change its name and ```docstring```. The bookkeeping is handled for us.

When it comes to type hinting things can get confusing very quick since the parameters and return types are both essentialy of the ```Callable``` type. To be properly generic, we'll use an upper-bound type definition to define a type, ```F```, which embraces any variation on callable objects or functions.

Let's look at the following example where we emphasize a situation where a decorator can come in handy. 
We want to log the time before a function is execute and then the end time after a function is executed. We could look at this as a cross-cutting concern. One option would be to manually log the time inside the function or right where the function is executed:

```Python
print(datetime.datetime.now())
result = function()
print(datetime.datetime.now())
```

or:

```Python
def function(): 
    print(datetime.datetime.now())
    # Implementation
    print(datetime.datetime.now())

function()
```

This is however very inconvinient and if we were talking about a real-world application, this would look a lot harder to maintain. This is where decorators come in to play.

We can use a decorator to wrap this function up and log the time automatically inside the decorator itself.

Example:G$

```Python
import functools
import datetime
from typing import Callable, TypeVar, cast, Any

FuncType = Callable[..., Any]
F = TypeVar('F', bound=FuncType)

def log_time(function:F) -> F:
    @functools.wraps(function)
    def logged_function(*args, **kwargs):
        print(datetime.datetime.now())
        function(*args, **kwargs)
        print(datetime.datetime.now())

    return cast(F, logged_function)


@log_time
def function(a, b):
    print(a+b)
```

The ```TypeVar``` function from the ```typing``` module represents a type variable. Type variables serve as the parameters for generic types as well as for generic function definitions. That type variable is bound to the ```Callable[..., Any]``` type which is stored in the ```FuncType``` variable. The ```Callable[..., Any]``` type hint represents a callable that takes in any number of arguments and returns ```Any``` kind of output.

We have used the ```@functools.wraps``` decorator to ensure that the wrapped up function keeps its name and ```docstring```.

## Parameterizing a decorator

When you want to give arguments to decorators, the process will look something like this:

```Python
@decorator(argument)
def function():
    pass
```

which is basically:

```Python
def function():
    pass

function = decorator(argument)(function)
```

Instead of ```function = decorator(function)``` we now added argument to our decorator, so it's ```function = decorator(argument)(function)```. You can obviously add more arguments to your decorator. Our decorator is not ```decorator``` anymore, our decorator will now be ```decorator(argument)```.

It's like writing:

```Python
concrete_decorator = decorator(argument)
function = concrete_decorator(function)
```

Here is how the implementation of a simple decorator with arguments and one without arguments looks like:

```Python
from typing import Callable, Any, TypeVar, cast
import functools

CallableFunction = Callable[..., Any]
F = TypeVar("F", bound=CallableFunction)


def normal_decorator(function: F) -> F:
    @functools.wraps(function)
    def wrapped_function(*args, **kwargs):
        print("Before function execution")
        function(*args, **kwargs)
        print("After function execution")

    return cast(F, wrapped_function)


def decorator_with_arguments(a: int, b: int) -> Callable[[F], F]:
    def concrete_decorator(function: F) -> F:
        @functools.wraps(function)
        def wrapped_function(*args, **kwargs):
            print("Before function execution. a -- > {0}".format(a))
            function(*args, **kwargs)
            print("After function execution. b -- > {0}".format(b))

        return cast(F, wrapped_function)

    return concrete_decorator


@decorator_with_arguments(1, 2)
def function():
    print("Inside the function")
```

> A decorator for a method of a class definition is identical to a decorator for a standalone function. While it's used in a different context, it will be defined like any other decorator. One small consequence of the different context is that we often, must explicitly name the ```self``` variable in decorators intended for methods.

## Creating a class decorator

When it comes to class decorators, there aren't many differences in comparison to function/method decorators. The essential rules are the same. The decorator is a function ( or a callable object ) that receives a class object as an argument and returns a class object as a result.

A simple class decorator is just like a function. All decorators are essentially the same. They must accept a function as an argument and be a callable object. All we have to do is to make our class a callable object and accept the function that is given to us in the constructor. Example:

```Python
class class_decorator:
    def __init__(self, function: F) -> None:
        self.function = function

    def __call__(self, *args, **kwargs):
        print("Before function execution")
        self.function(*args, **kwargs)
        print("After function execution")


@class_decorator
def function(*args):
    print("Inside the function. Arguments given to the function : {0}".format(args))
```

When it comes to giving argument to a class decorator, things very similar as well. Here is an example:

```Python
def class_decorator_with_arguments(*class_args, **class_kwargs):
    class concrete_decorator_class:
        def __init__(self, function, *args, **kwargs):
            self.function = function
            self.class_args = class_args
            self.class_kwargs = class_kwargs

            print(self.function)
            print(self.class_args)
            print(self.class_kwargs)

            """
            Console output here:

            <function function at 0x7fef5a429ee0>
            (1, 2)
            {'a': 3, 'b': 7}
            """

        def __call__(self, *function_args, **function_kwargs):
            print("Before function execution. Class args : {0}".format(self.class_args))
            self.function(*function_args, **function_kwargs)
            print(
                "After function execution. Class kwargs : {0}".format(self.class_kwargs)
            )

    return concrete_decorator_class


@class_decorator_with_arguments(1, 2, a=3, b=7)
def function(*args, **kwargs):
    print("Inside the function. Arguments given to the function : {0}".format(args))
```

The ```function``` will be given automatically to the class. After the function was given to the class, the ```*class_args``` and ```**class_kwargs``` arguments are next.

## ```__init_subclass__```

From the python [data model documentation for ```__init_subclass__```](https://docs.python.org/3/reference/datamodel.html#object.__init_subclass__()) we can see that the ```__init_subclass__(cls)``` method is called whenever the containing class is subclassed. It is only called once, when it is subclassed, it is not called for every single instance. It can be used in order to add certain functionality to certain subclasses based on some arbitrary criteria.

```Python
class BaseClass:
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        cls.special_property_from_init_subclass = 4
    
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b


class Test(BaseClass):
    def __init__(self, a: int, b: int, c: int) -> None:
        super().__init__(a, b)
        self.c = c


test = Test(1, 2, 3)
print(test.a)
print(test.b)
print(test.c)
print(test.special_property_from_init_subclass)

"""
Output:

1
2
3
4
"""
```

---
---

# Section 2

---

# 10.  Serializing and Saving - JSON, YAML, Pickle, CSV and XML

## Introduction

In order to make a Python object persistent we must convert it to bytes and save the bytes to a file. We call this process ***serialization*** ( also called *marshaling*, *deflaiting* or *encoding* ). We will look at several ways to serialize a Python object to a stream of bytes. It's important to note that we are focusing on representing the state of the object, disregarding the class that it's made from, its methods and superclasses.

A serialization scheme includes a **physical data format**. Each format offers some advantages and disadvantages. There is no *best* format to represent the state of objects.

## Understanding persistence, class, state and representation

Generally, python objects only exist in *volatile* computer memory. This is constrained even more by objects that only exist if there are references to it ( otherwise they would get deleted by garbage collectors ). In order to save the state of an object, we have to make it persistent. The same serialization techniques apply if we want to transfer the state of the object from a process to another process. 

Most operating systems offer persistent stoarge in the form of a filesystem. This can be disk drivers, flash drives or any other form of *non-volatile* storage. Persisting the bytes from the memory to the filesystem turns out to be quite a difficult process.

The complexity arises because the objects that we want to make persistent have references to other objects. An object belongs for example to a class. The class will contain one if not several subclasses. If the object is used as a container, it has references to all the items that it contains. References are based on the locations in memory, which are not fixed.

Objects that are referenced to the objects that we want to persist are largely static. Class definitions change much slower compared to instance variables within an object. Serialization techniques focus on persisting the dynamic state of an object based on its instance variables.

> We don't actually have to do anything extra to persist class definitions; we already have a very simple method for handling classes. Class definitions exist primarily as source code. The calss definition in the volatile memory is rebuilt from the source ( or the byte-code version of the source ) every time it's needed. If we need to exchange a class definition, we exchange Python module or packages.

## Common Python terminology

Python serialization terminology focuses on the words *dump* and *load*:

* ```dump(object, file)```: This method will dump the given object to a file
* ```dump(object)```: This will dump an object and return the string representation of it
* ```load(file)```: This will load an object from a file, returning the constructed object.
* ```loads(string)```: This will load an object from a string representation, returning the constructed object.

This is not a formal standard. The method names are not guaranteed by any ABC inheritance or mixin class definition.

## Filesystem and network considerations

Since the OS filesystem and the network work in bytes, we need to find a way to represent our objects in bytes. This is a two step process. The first step involves around transforming our object into a string. The second step is to use the Python ```str``` class to encode the string for us. Most serialization methods focus on creating strings.

When we look at the OS filesystems, we can see two types of devices: ```block-mode``` and ```character-mode``` devices. *Block-mode* devices are also called *seekable* because the OS supports a seek operation that can access any byte in the file in an arbitrary order. Character-mode devices are not seekable. They are interfaces where bytes are transmitted serially. Seeking would involve some kind of time travel to recover past bytes or see futures bytes.

> This distinction between the *character* and *block* mode can have an impact on how we represent the state of a complex object or a collection of objects. The serializations we'll look at in this chapter focus on the simplest common feature set: an ordered stream of bytes. The stream of bytes can be written to either kind of device.

## The problem with extending sequence classes

When we extend sequence classes we might get confused with some serialization algorithms. This may wind up bypassing the extended features we put in a subclass of a sequence. Wrapping a sequence or inventing a new one is usually a better idea than extending it.

## Dumping and loading with JSON

**JSON ( JavaScript Object Notation )** is a wiedely use data-interchange format. It is used by a lot of programming languages ( especially JavaScript ) and it even has databases that run only on JSON data ( *CouchDB* for example ). JSON documents are easy to read and easy to edit manually.

The ```json``` module works with built-in Python types. It doesn't work directly with classes if we don't help it a little. Here is a table that illustrates JSON/JavaScript types mapped to Python types:

|Python type|JSON|
|-----------|----|
|```dict```|```object```|
|```list, tuple```|```array```|
|```str```|```string```|
|```int, float```|```number```|
|```True```|```true```|
|```False```|```false```|
|```None```|```null```|

**Values that are not on the python column that you want to save in JSON format must be coerced to one of the available JSON/JavaScript types. This is often done via extension functions that we can plug into the ```dump()``` and ```load()``` functions.**

### Supporting JSON in our classes

In order to support creating strings in JSON we need encoders and decoders for classes outside the types that can be converted automatically ( see table above ).
***In order to encode a unique object into JSON we need to provide a function that will reduce our objects to Python primitive types that can be easily converted to JSON. The ```json``` module calls this a default function; it provides a default encoding for an object of an unknown class.***

In order to decode strings in JSON and create Python objects of an application class, a class outside the baseline types supported by JSON, we need to provide an extra function. 
***This function will transform a dictionary of Python primitive values into an instance of the one of our application classes. This is called the object hook function; it's used to transform ```dict``` into an object of a customized class.***

The ```json``` module documentation suggests that we should make use of class hinting. Their suggestiong is to encode an instance of a customized class as a dictionary:

```{"__jsonclass__": ["ClassName", [param1, ...]]}```

The value associated with ```__jsonclass__``` is a list of two items: the class name, and a list of arguments required to create and instance of that class.

> In order to decode an object from a JSON dictionary, an object hook function can look for the ```__jsonclass__``` key as a hint that one of our classes needs sto be built, not a built-in Python object. The class name can be mapped to a class object and the argument sequence can be used to build the instance.

### Customizing JSON encoding

For class hinting we will provide three pieces of information. 
We will have a ```__class__``` key that will include the name of the class.
We will have an ```__args__``` key that will store all the positional arguments.
We will have a ```__kwargs__``` key that will store all the keyword arguments.

Let's take a look at the following example. We have a class ```Post``` that looks like this:

```Python
from dataclasses import dataclass
import datetime
from typing import Dict, Any, List


@dataclass
class Post:
    date: datetime.datetime
    title: str
    rst_text: str
    tags: List[str]

    def as_dict(self) -> Dict[str, Any]:
        return dict(
            date=str(self.date),
            title=self.title,
            underline="-" * len(self.title),
            rst_text=self.rst_text,
            tag_text=" ".join(self.tags),
        )
```

We also have a class ```Blog``` that extends from ```list``` and looks like this:

```Python
from typing import DefaultDict, List, Dict, Any, Optional
from Post import Post
from collections import defaultdict


class Blog(list):
    def __init__(self, title: str, posts: Optional[List[Post]] = None) -> None:
        self.title = title
        super().__init__(posts if posts is not None else [])

    def as_dict(self) -> Dict[str, Any]:
        return dict(title=self.title, entries=[p.as_dict() for p in self])
```

An encode for the ```Blog``` object would look like this:

```Python
def blog_encode(object: Any) -> Dict[str, Any]:
    if isinstance(object, datetime.datetime):
        return dict(
            __class__="datetime.datetime",
            __args__=[],
            __kw__=dict(
                year=object.year,
                month=object.month,
                day=object.day,
                hour=object.hour,
                minute=object.minute,
                second=object.second,
            ),
        )
    elif isinstance(object, Post):
        return dict(
            __class__="Post",
            __args__=[],
            __kwargs__=dict(
                date=object.date,
                title=object.title,
                rst_text=object.rst_text,
                tags=object.tags,
            ),
        )
    elif isinstance(object, Blog):
        return dict(
            __class__="Blog", __args__=[object.title, object.posts], __kwargs__={}
        )
    else:
        return object
```

This function shows us two different flavors of object encodings for the three classes:

* We encoded a ```datetime.datetime``` object as a dictionary of individual fields using keyword arguments.
* We encoded a ```Post``` instance as a dictionary of individual fields, also using keyword arguments.
* We encoded a ```Blog``` instance as a sequence of title and post entries using a sequence of positional arguments.

The ```else``` statement returns the raw object. This object will be encoded by the ```json```'s module default encoding. This could be for example primitive values. If values are given that are not primitive and can't be encoded by the default encoder, an exception will be thrown.

We can now use this function in order to encode as follows:

```Python
import datetime
import json

travel = Blog("Travel")
travel.append(
    Post(
        date=datetime.datetime(2013, 11, 14, 17, 25),
        title="Test Title 1",
        rst_text="""some text""",
        tags=["#test", "#this_is_a_tag"],
    )
)
travel.append(
    Post(
        date=datetime.datetime(2013, 11, 18, 15, 30),
        title="Test Title 2",
        rst_text="""some text 2""",
        tags=["#test2", "#this_is_a_tag_2"],
    )
)

text = json.dumps(travel, indent=4, default=blog_encode)
print(text)
```

Our json string will now be successfully encoded and will look like this:

```JSON
[
    {
        "__class__": "Post",
        "__args__": [],
        "__kwargs__": {
            "date": {
                "__class__": "datetime.datetime",
                "__args__": [],
                "__kw__": {
                    "year": 2013,
                    "month": 11,
                    "day": 14,
                    "hour": 17,
                    "minute": 25,
                    "second": 0
                }
            },
            "title": "Test Title 1",
            "rst_text": "some text",
            "tags": [
                "#test",
                "#this_is_a_tag"
            ]
        }
    },
    {
        "__class__": "Post",
        "__args__": [],
        "__kwargs__": {
            "date": {
                "__class__": "datetime.datetime",
                "__args__": [],
                "__kw__": {
                    "year": 2013,
                    "month": 11,
                    "day": 18,
                    "hour": 15,
                    "minute": 30,
                    "second": 0
                }
            },
            "title": "Test Title 2",
            "rst_text": "some text 2",
            "tags": [
                "#test2",
                "#this_is_a_tag_2"
            ]
        }
    }
]
```

### Customizing JSON decoding

In order to decode objects from a string into JSON notation we need to workt within the structure of a JSON parsing.

Objects were encoded in ```dict```s. That means that every ```dict``` decoded by the JSON decoder *could* be one of our customized classes.

> The JSON decode *object hook* is a function that's invoked for each ```dict``` to see whether it represents a customized object. If ```dict``` isn't recognized by the ```hook``` function, it's an ordinary dictionary and shoul be returned without modification.

Here is how our object hook function will look like:

```Python
def blog_decode(some_dict: Dict[str, Any]) -> Dict[str, Any]:
    if set(some_dict.keys()) == {"__class__", "__args__", "__kwargs__"}:
        class_ = eval(some_dict["__class__"])
        return class_(*some_dict["__args__"], **some_dict["__kwargs__"])
    else:
        return some_dict


blog_data = json.loads(text, object_hook=blog_decode)
print(blog_data)
```

This will decode a string, encoded in the JSON notation, using our object hook function in order to transform ```dict``` into proper ```Blog``` and ```Post``` objects.

The output will be:

```Python
{'__class__': 'datetime.datetime', '__args__': [], '__kwargs__': {'year': 2013, 'month': 11, 'day': 14, 'hour': 17, 'minute': 25, 'second': 0}}

{'__class__': 'Post', '__args__': [], '__kwargs__': {'date': datetime.datetime(2013, 11, 14, 17, 25), 'title': 'Test Title 1', 'rst_text': 'some text', 'tags': ['#test', '#this_is_a_tag']}}

{'__class__': 'datetime.datetime', '__args__': [], '__kwargs__': {'year': 2013, 'month': 11, 'day': 18, 'hour': 15, 'minute': 30, 'second': 0}}

{'__class__': 'Post', '__args__': [], '__kwargs__': {'date': datetime.datetime(2013, 11, 18, 15, 30), 'title': 'Test Title 2', 'rst_text': 'some text 2', 'tags': ['#test2', '#this_is_a_tag_2']}}

[Post(date=datetime.datetime(2013, 11, 14, 17, 25), title='Test Title 1', rst_text='some text', tags=['#test', '#this_is_a_tag']), Post(date=datetime.datetime(2013, 11, 18, 15, 30), title='Test Title 2', rst_text='some text 2', tags=['#test2', '#this_is_a_tag_2'])]

```

## Refactoring the encode function

Look at our encoding function that are a lot of things that we could improve when it comes to reusability, maintainability and the design and structure of our code. ***The encoding function shouldn't expose information on the classes being converted into JSON.*** In order to keep each class properly encapsulated it's better if we would have a way of getting our JSON encoding from a specific class, from that particular class, rather than from the *default* function needed to encode those classes.

In that case, we can make a getter for every class that we want to encode that just returns the encoded version of the instance at hand.

Example for the ```Blog``` class:

```Python
class Blog(list):
    def __init__(self, title: str, posts: Optional[List[Post]] = None) -> None:
        self.title = title
        super().__init__(posts if posts is not None else [])

    def as_dict(self) -> Dict[str, Any]:
        return dict(title=self.title, posts=[p.as_dict() for p in self])

    @property
    def _json(self) -> Dict[str, Any]:
        return dict(
            __class__ = self.__class__.__name__,
            __kwargs__ = {},
            __args__ = [self.title, self.posts]
        )
```

We have added a property to our class now that returns a dictionary that will be needed for encoding instance of this class. It returns, just like in our previous encoding function, a dictionary with the class name, the args and the kwargs.

Here is our refactored ```Post``` class:

```Python
@dataclass
class Post:
    date: datetime.datetime
    title: str
    rst_text: str
    tags: List[str]

    def as_dict(self) -> Dict[str, Any]:
        return dict(
            date=str(self.date),
            title=self.title,
            underline="-" * len(self.title),
            rst_text=self.rst_text,
            tag_text=" ".join(self.tags),
        )

    @property
    def _json(self) -> Dict[str, Any]:
        return dict(
            __class__ = self.__class__.__name__,
            __kwargs__ = dict(
                date = self.date,
                title = self.title,
                rst_text = self.rst_text,
                tags = self.tags
            ),
            __args__ = []
        )
```

Now that we have refactored those classes and have made it self to encode them, we can now refactor our *default* function:

```Python
def blog_encode(obj: Union[Blog, Post, Any]) -> Dict[str, Any]:
    if isinstance(obj, datetime.datetime):
        return dict(
            __class__ = "datetime.datetime",
            __args__ = [],
            __kwargs__ = dict(
                year=obj.year,
                month=obj.month,
                day=obj.day,
                hour=obj.hour,
                minute=obj.minute,
                second=obj.second,
            )
        )
    else:
        try:
            encoding = obj._json
        except AttributeError:
            encoding = json.JSONEncoder().default(obj)

        return encoding
```

In this refactored *default* function we first check to see if the object that we are trying to encode is a ```datetime.datetime``` object since we didn't want to extend this type of class and add a json encoder getter to it, so we will do it manually because there are also no security risks. There is no point in encapsulating this class. The next things that we encode are the objects that have a json getter encoder to them, which in our case is an object that has the ```._json``` property. If that is not the case for the object then we will encode it using the default encoder.

### Writing/Loading JSON to/from a file

When it comes to writing/loading json to/from a file it is very easy. You just use the common terminology and methods that we have used up to this point.

Here is an example of how to dump and load json:

```Python
# DUMP

with Path("temp.json").open("w", encoding="utf-8") as target:
    json.dump(travel, target, default=blog_encode)
```

```Python
# LOAD

with Path("temp.json").open(encoding="utf-8") as source:
    objects = json.load(source, object_hook=blog_decode)
```

## Dumping and loading with YAML

The [official yaml web page](https://yaml.org) states the following about YAML:

> YAML™ (rhymes with “camel”) is a human-friendly, cross language, Unicode based data serialization language designed around the common native data types of dynamic programming languages.

The Python Standard Library documentation for the ```json``` module explains the following about JSON and YAML:

>JSON is a subset of YAML 1.2. The JSON produced by this module's default settings is also a subset of YAML 1.0 and 1.1. This module can thus also be used as a YAML serializer.

We can tehnically use the ```json``` module for YAML. The ```json``` module however cannot be used in order to decode sophisticated YAML data.

There are 2 advantages when it comes to using YAML:

1. YAML is a more sophisticated notation, which allows us to encode additional details about our objects.
2. The [PyYAML](https://pyyaml.org/) implementation has a deep level of integrati on with Python that allows us to very simply create YAML encodings of Python objects. 

***The drawback of YAML is that it is not as widely used as JSON.***

### Working with PyYAML

Once you have installed the package ( using pip ) you can start working with PyYAML. The PyYAML and ```json``` modules have a lot of things in common of course. Here is for example how you encode an object using YAML:

```Python
import yaml
text = yaml.dump(travel)
print(text)
```

And here is how the YAML encoding of our complex Python object looks like:

```YAML
!!python/object/new:__main__.Blog
listitems:
- !!python/object:__main__.Post
  date: 2013-11-14 17:25:00
  rst_text: some text
  tags:
  - '#test'
  - '#this_is_a_tag'
  title: Test Title 1
- !!python/object:__main__.Post
  date: 2013-11-18 15:30:00
  rst_text: some text 2
  tags:
  - '#test2'
  - '#this_is_a_tag_2'
  title: Test Title 2
state:
  title: Travel
```

The output is very complex and we can also easily edit a YAML file in order to make changes. 
The class names are encoded with YAML **```!!```** tags. YAML contains 11 standard tags. The ```yaml``` module includes a lot of Pyton-specific tags and five *complex* Python tags.

> The Python class names are qualified by the defining module. In our case, the module happened to be a simpel script, so the class names are ```__main__.Blog``` and ```__main__.Post```. If we had imported these from another module, the class names would reflect the module that defined the classes.
> Items in a list are shown in a block sequence form .Each item starts with a -sequence; the rest of hte items are indented with two spaces. When ```list``` or ```tuple``` is small enough, it can flow onto a single line.

### Formatting YAML data on a file

We have several formatting options to create a prettier YAML representation of our data. Here is a table with some of the options:

|Option|Description|
|------|-----------|
|```explicit_start```|If ```true```, writes a ```---``` marker before each object.|
|```explicit_end```|If ```true```, writes a ... marker after each object. We might use this or ```explicit_start``` if we're dumping a sequence of YAML documents into a single file and need to know when none ends and the next begins.|
|```version```|Given a pair of integers ```(x, y)```, writes a ```%YAML x.y``` directive at the beginning. This should be ```version = (1, 2)```|
|```tags```|Given a mapping, it emits a YAML ```%TAG``` directive with different tag abbreviations|
|```canonical```|If ```true```, includes a tag on every piece of data. If ```false```, a number of ```tags``` are assumed.|
|```indent```|If set to a number, changes the indentation used for blocks.|
|```width```|If set to a number, changes the ```width``` at which long items are wrapped to multiple, indented lines.|
|```allow_unicode```|If set to ```true```, permits full Unicode without escapes. Otherwise, characters outside the ASCII subset will have escapes applied.|
|```line_break```|Uses a different line-ending characters; the default is a newline.|

### Extending the YAML representation

Sometimes we might want to change the way our class encoding looks like in YAML. Our representation might look better than what YAML has to offer us.

The ```yaml``` module, just like the ```json``` module includes some methods/functions that help you customize your encoding/decoding of custom objects. The ```representer``` is used to create a YAML representation, including a tag and value. The ```constructor``` is used to build a Python object fro mthe given value.
These functions are just like the *default* and *object hook* functions from the ```json``` module.

Let's take a look at the following example:

```Python
from enum import Enum
from typing import Optional, Any
import yaml


class Suit(str, Enum):
    Clubs = "♣"
    Diamonds = "♦"
    Hearts = "♥"
    Spades = "♠"


class Card:
    def __init__(
        self,
        rank: str,
        suit: Suit,
        hard: Optional[int] = None,
        soft: Optional[int] = None,
    ) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __str__(self) -> str:
        return f"{self.rank!s}{self.suit.value!s}"


class AceCard(Card):
    def __init__(self, rank: str, suit: Suit) -> None:
        super().__init__(rank, suit, 1, 11)


class FaceCard(Card):
    def __init__(self, rank: str, suit: Suit) -> None:
        super().__init__(rank, suit, 10, 10)
```

Here is what these objects look like after we dump them into the YAML format using the default serialization:

```YAML
!!python/object:__main__.AceCard
hard: 1
rank: 1
soft: 11
suit: !!python/object/apply:__main__.Suit
- "\u2663"

!!python/object:__main__.Card
hard: null
rank: 2
soft: null
suit: !!python/object/apply:__main__.Suit
- "\u2666"

!!python/object:__main__.FaceCard
hard: 10
rank: 10
soft: 10
suit: !!python/object/apply:__main__.Suit
- "\u2660"
```

The representation is correct but maybe a bit too wordy. We might want to change this and make a custom serializer.

As previously mentioned, we can create ```representer``` functions that customize the serialization process for us.
Here is an example of 3 representers for our cards:

```Python
def card_representer(dumper: Any, card: Card) -> str:
    return dumper.represent_scalar(
        "!Card", f"{card.rank!s}{card.suit.value!s}"
    )

def acecard_representer(dumper: Any, card: Card) -> str:
    return dumper.represent_scalar(
        "!AceCard", f"{card.rank!s}{card.suit.value!s}"
    )

def facecard_representer(dumper: Any, card: Card) -> str:
    return dumper.represent_scalar(
        "!FaceCard", f"{card.rank!s}{card.suit.value!s}"
    )

yaml.add_representer(Card, card_representer)
yaml.add_representer(AceCard, acecard_representer)
yaml.add_representer(FaceCard, facecard_representer)
```

> We have now represented each ```Card``` instance as a short string. YAML includes a tag to show which class should be built from the string. All three classes use the same format string. This happens to match the ```__str__()``` method, leading to a potential optimization.

This is how the YAML representation of our cards will look now:

```YAML
!AceCard "1\u2663"

!FaceCard "11\u2666"

!Card "2\u2665"
```

Just like the ```json``` module we also have a function that decodes/constructs objects from parsed documents. In the ```json``` module we call this function the *object hook* function but in YAML we call it a *constructor*.

Here is an example of how our constructors could look like:

```Python
def card_constructor(loader: Any, node: Any) -> Card:
    value = loader.construct_scalar(node)
    rank, suit = value[:-1], value[-1]
    return Card(rank, suit)

def acecard_constructor(loader: Any, node: Any) -> Card:
    value = loader.construct_scalar(node)
    rank, suit = value[:-1], value[-1]
    return AceCard(rank, suit)

def facecard_constructor(loader: Any, node: Any) -> Card:
    value = loader.construct_scalar(node)
    rank, suit = value[:-1], value[-1]
    return FaceCard(rank, suit)

yaml.add_constructor("!Card", card_constructor)
yaml.add_constructor("!AceCard", acecard_constructor)
yaml.add_constructor("!FaceCard", facecard_constructor)
```

Let's take a look now at how our representers and constructor have helped us:

```Python
deck = [
    AceCard(1, Suit.Clubs),
    FaceCard(11, Suit.Diamonds),
    Card(2, Suit.Hearts)
]
text = yaml.dump(deck, allow_unicode=True)
print(text)
objects = yaml.load(text, Loader=yaml.Loader)
print(objects)
```

The output:

```YAML
- !AceCard '1♣'
- !FaceCard '11♦'
- !Card '2♥'
```

```Python
[<__main__.AceCard object at 0x7fafe78cce20>, <__main__.FaceCard object at 0x7fafe78cc910>, <__main__.Card object at 0x7fafe78cc850>]
```

### Security and safe loading

YAML can mostly build objects of any type. This allows an attack on an application that transmits YAML files over the internet without proper SSL controls.

YAML has a function called ```safe_load()``` that refuses to execute arbitrary Python code as part of building an object. This however severly limits what can be loaded.

A better approach would be too use the mixin class ```yaml.YAMLObject``` for our own objects. We use this to set some class-level attributes that provide hints to ```yaml``` and ensure the safe construction of objects.

You can define a class for safe transmission this way:

```Python
class Card(yaml.YAMLObject):
    yaml_tag = "!Card"
    yaml_loader = yaml.SafeLoader
```

> The two attributes will alert ```yaml``` that these objects can be safely loaded without executing arbitrary and unexpected Python code. Each subclass of ```Card``` only has to set the unique YAML tag that will be used.

Example:


```Python
class AceCard(Card):
    yaml_tag = "!AceCard"
```

> With these modification to the class definitions, we can now use ```yaml.safe_load()``` on the YAML stream without worrying about the document having malicious code inserted over an unsecured internet connection. The explicit use of the ```yaml.YAMLObject``` mixin class for our own objects coupled with setting the ```yaml_tag``` attribute has several advantages. It leads to slightly more compact files. It also leads to a better-looking YAML files--the long, generic tags are replaced with shorter tags.

## Dumping and Loading using pickle

The ```pickle``` module is Python's native format to make objects persistent.
The Python Standard Library says this about ```pickle```:

> The pickle module can transform a complex object into a byte stream and it can transform the byte stream into an object with the sam internal structure. Perhaps the most obvious thing to do with these byte stream is to write them onto a file, but it is also conceivalbe to send them across a network or store them in a database.

The ```pickle``` module ***only focuses on Python***. It is not like other formats, like CSV, JSON or YAML where data is interchangeable between multiple platforms and programming languages. ***In this case, the focus is only on Python.***

The ```pickle``` module is also tightly integrated with Python. We have special methods that allow us to integrate our custom classes with ```pickle``` with ease while keeping a clean class design and maintanable code. Some of these special methods are ```__reduce__()``` and ```__reduce_ex__()``` that help a class to support the ```pickle``` processing.

This is how we dump and load objects with ```pickle```:

```Python
# DUMPING
with Path("test.p").open("wb") as target:
    pickle.dump(travel, target)
```

```Python
# LOADING
with Path("test.p").open("rb") as source:
    obj = pickle.load(source)
```

The pickled data is written in bytes, that means that if we want to write or read something from a file of that type, we have to open it in binary mode. The underlying stream of bytes is not intended for human consumption.

### Designing a class for reliable pickle processing

***When unpickling an object, the ```__init__()``` method is completely ignored. The ```__init__()``` method is bypassed by using the ```__new__()``` method instead, where the object is created. The properties of our object are set directly in the ```__dict__``` property.***

***This is a problem for when we have some processing in our ```__init__()``` method. If we want to open a GUI or start a certain process in our ```__init__()``` method, these processes won't be executed at all since the ```__init__()``` method is bypassed by the ```__new__()``` method.***

A class that relies on processing during ```__init__()``` has to make special arrangements to be sure that that this initial processing will be executed properly. There are two things that we can do:

* Avoid eager startup processing in ```__init__()```. Instead, do only the minimal initialization processing. For example, if there are external file operations, these should be deferred until required. If there are any eager summarization computations, they must be redesigned to be done lazily. Similarly, any initialization logging will not be executed properly.
* Define the ```__getstate__()``` and ```__setstate__()``` methods that can be used by ```pickle``` to preservet hte state and restore the state. The ```__setstate__()``` method can then invoke the same method that ```__init__()``` invokes to perform a one-time initialization processing in ordinary Python code.


***When we pickle an object, we pickle it at a certain state. Let's say that we have an object that contains the properties ```a``` and ```b``` and we have ```object.a = 1``` and ```object.b = 2```. When we pickle this object, we pickle it at that specific state, which is a state after initialization. We cannot have an object that exists at an uninitialized state. All objects are initialized. That happens through the ```__new__()``` process, which creates the object itself in memory, followed by the ```__init__()``` process which is the initialization process, which gives the object meaning, it gives the objects its arbitrary properties ( if there are any ).***

***When we unpickled an object, we use the pickled information about that object in order to built a new object that is exactly like the object that we have just unpickled ( exactly how we have proceded up to this point ). When we unpickle an object however, we unpickled it at the state that it was when we've pickled it. That means that we will unpickle an initialized object. That also means that we will not go over the ```__init__()``` method. We will just build the object in memory using the ```__new__()``` method and then we will give its attributes directly using the ```__dict__``` property.***

***That means that every process that we have intended to start in the initialization method will not start when unpickling since we are not re-initializing the object, since we are unpickling an object that was pickled at an already-initialized state***.

Here is the documentation of ```__getstate__()``` and ```__setstate__(state)```:

```object.__getstate__()``` documentation:
> Classes can further influence how their instances are pickled; if the class defines the method ```__getstate__()```, it is called and the returned object is pickled as the contents for the instance, instead of the contents of the instance’s dictionary. If the ```__getstate__()``` method is absent, the instance’s ```__dict__``` is pickled as usual.

```object.__setstate__(state)``` documentation:
> Upon unpickling, if the class defines ```__setstate__()```, it is called with the unpickled state. In that case, there is no requirement for the state object to be a dictionary. Otherwise, the pickled state must be a dictionary and its items are assigned to the new instance’s dictionary. If ```__getstate__()``` returns a false value, the ```__setstate__()``` method will not be called upon unpickling.

Here is a practical example:

```Python
import logging
import pickle
from typing import Dict, Any

logger = logging.Logger(__name__)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


class TestClass:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

        self.sum = self.a + self.b
        logger.debug("Initialization log.")

    def __getstate__(self) -> Dict[str, Any]:
        return vars(self)

    def __setstate__(self, state: Dict[str, Any]) -> None:
        # Update the dict of our object since it's empty and we are updating it with the state of the unpickled object
        self.__dict__.update(state)
        logger.debug("Unpickling log")


test = TestClass(1, 2)
pickled_test = pickle.dumps(test)
print(pickled_test)
unpickled_test = pickle.loads(pickled_test)
print(unpickled_test)
print(unpickled_test.a)
```

> The ```__getstate__()``` method is used while pickling to gather the current state of hte object. This method can return anything. In the case of objects that have internal memoization caches, for example, the cache might not be pickled in order to save time and space. This implementation uses the internal ```__dict__``` without any modification.
> The ```__setstate__(state)``` method is used while unpickling to reset the value of the object. This version merge the state into the internal ```__dict__``` and then writes the appropriate logging entries.

### Security and the global issue

> During unpickling, a global name in the pickle stream can lead to the evaluation of arbitrary code. Generally, the global names inserted into the bytes are class names or a function name. However, it's possible to include a global name that is a function in a module such as ```os``` or ```subprocess```. This allows an attack on an application that attempts to transmit pickled objects through the internet without strong SSL controls in place.

In order to prevent the execution of arbitrary code we must extend the ```pickle.Unpickler``` class. We'll override the ```find_class()``` method to replace it with something more secure. We have to account for several unpickling issues, such as the following:

* We have to prevent the use of the built-in ```exec()``` and ```eval()``` functions.
* We have to prevent the use of modules and packages that might be considered unsafe. For example, ```sys``` and ```os``` should be prohibited.
* We have to permit the use of our application modules.

Here is an example that imposes some restrictions on our unpickled data:

```Python
import builtins
import pickle
from typing import Any


class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module: str, name: str) -> Any:
        if module == "builtins":
            if name not in ("exec", "eval"):
                return getattr(builtins, name)
        elif module in ("__main__", "my_personal_modules"):
            # Valid module names depends on execution context
            return globals()[name]
        raise pickle.UnpicklingError(
            f"global '{module}.{name}' is forbidden"
        )
```

## Dumping and loading with CSV

CSV files are not really a complete persistene solution to python objects. The encode and decode ***very***  simple ```list``` or ```dict``` instances into CSV notation.

Working with CSV files means that you have to do a lot of manual mapping between very complex python objects and very simple CSV files. We must always remain cognizant of the limitations of CSV files.

CSV data only contains pure text. There is on such thing as data types or data structures. It is only pure text. This makes it ***extremly*** difficult to establish a powerful and maintainable connection between complex python objects and the CSV notation. CSV files are also often touched manually and can easily become incompatible because of human tweaks.

> When we have relatively simple class definitions, we can often transofrm each instance into a simple, flat row of data values. Often, ```NamedTuple``` is a good match between a CSv source file and Python objects. Going the other way, we might need to design our Python classes around ```NamedTuple``` if our application will save data in the CSV notation.

### Dumping simple sequences to CSV.

An ideal mapping, as previously mentioned, is between ```NamedTuple``` instances and rows in a CSV file. Each row represents a different ```NamedTuple```.

An example:

```Python
from typing import NamedTuple

class GameStat(NamedTuple):
    player: str
    bet: str
    round: int
    final: float
```

You can now use the CSV ```DictWriter``` from the ```csv``` module in order to write this to a CSV file.

## Dumping and loading with XML

XML, just like JSON is not a complete persistence solution for Python objects. The ```xml``` package includes numerous modules that help you work with XML, including a **Document Object Model ( DOM )** that works just like the DOM in HTML.

Working with XML objects, just like working with CSV objects involves a manual mapping between python objects and xml structures. We need to remain mindful of XML's constraints. The content of an XML attribute or tag is pure text. When loading XML content, we need to manually convert all the values into useful types in our application. We might have attributes or tags that indicate the expected type.

When we look at dumping a  Python object to create an XML document, there are three common ways to build the text:

* **Include XML output methods in our class design.** In this case, our classes emit strings that can be assembled into an XML document. This conflates serialization into the class in a potentially brittle design.
* **Use ```xml.etree.ElementTree``` to build the ```ElementTree``` ndoes and return this structure: This can be then rendered as text. This is somewhat less brittle because it builds an abstract document object model rather than text.
* **Use an external template and fill attributes into that template**: Unless we have a sophisticated template tool, this doesn't work out well. The ```string.Template``` class in the standard library is only suitable for very simple objects. More generally, Jinja2 or Mako should be used. 

> There are some projects that include generic Python XML serializers. The problem with trying to create a generic serializers is that XML is extremly flexible; each application of XML seems to have unique **XML Schema Definition ( XSD )** or **Document Type Definition ( DTD )**.

# 11. Storing and Retrieving Objects via Shelve

## CRUD operations and multi-tier architecture

Applications that contain persistent objects may demonstrate four cases, summarized as **CRUD operations**: *create*, *retrieve*, *update* and *delete*. The idea is that any of these operations can be applied to any object in the domain; this leads to the need for a more sophisticated persistence mechanism than a monolithic load or dump.

When using more sophisticated storage this always leads to the allocation of reponsability in our application. There are certain higher-level design patterns that help us with that, one of them being the **multi-tier architecture*:

* **Presentation layer**: This includes web browsers, GUIs for a locally-installed application.
* **Application layer**: This layer is often based on a web-server but it can also be a portion of a locally-installed software. The application layer can be usefully subdivided into a processing layer and a data model layer. The processing layer involves the classesa and functions that embody an application's behavior. The data model layer defines the problem domain's object model.
* **Data layer**: This can be further subdivided into an access layer and a persistence layer. The access layer provides uniform access to persistent objects. The persistence layer serializes objects and writes them to the persistent storage. The is where the more sophisticated storage techniques are implemented

Since each of these layers can be subdivided into multiple layers themselves there are a number of variations of this architecture. It can also be called a three-tier architecture. It can also be called an **n-tier architecture** if you want to build more layers.

The data layer can use modules that help with persistence such as ***```shelve```***. This module defines a mapping-like container in which we can store objects. Each stored object is written and pickled to a file. We can also unpickle and retrieve any object from the file.

## Analyzing persistent object use cases.

When we a large problem domain where with many persistent, independent and mutable objects we have to introduce some more depth to the use cases:

* **We might not want to load all the objects into our memoy**. When it comes to *big data* it might also be impossible to do so.
* **We may only update a small subset of objects from our problem domain**. Loading and then dumping all the persistent objects in order to update only one single object can become highly inefficient.
* **We may not be dumping all the objects at one time; we may be accumulating objects incrementally.** Some format,s such as YAML and CSV, allow us to append themselves to a file with little complexity. Other formats, such as JSON and XML, have terminators that make it difficult to simply append to a file. 

It is common to look at serialization, transactional consistentcy, as well as concurrent write access and put them all in the concept of *database*. The ```shelve``` module is not a comprehensive database solution by itself.

## The ACID properties

The design of our application must consider the implication of the **ACID properties** to our ```shelve``` database.

An application often makes chnages in bundles of related operations. This bundle of operations **must** change the database **from one consistent state to the next consistent state**. The intent of these bundles is to ensure that the database is protected from an unconsistent state.

The ACID properties characterize how we want the database transactions to behave as a whole:

* **Atomicity**: A transaction must be atomic. If there are multiple operations within a transaction, either all the operations should be completed or none of them should be completed. It should never be possible to view a pratially completed transaction.
* **Consistency**: A transaction must assure consistency of the overall database. It must change the database from one valid state to another. A transaction should not corrupt the database or create inconsistent views among concurrent users. All users see the same net effect of completed transactions.
* **Isolation**: Each transaction should operate as if it processed in complete isolation from all other transactions. We can't have two concurrent users interfering with each other's attempted updated. We should always be able to transform concurrent access into (possible slower) serial access and the database updated will produce the same results. Locks are often used to achieve this.
* **Durability**: The changes to the database should persist properly in the filesystem.

## Creating a shelf

In order to create a shelf using the ```shelve``` module you first must open a persisten shelf structure using ```shelve.open()```. The second step would be to close the file properly so that all changes will be written to the underlying filesystem.

The ```shelve.open()``` function requries two parameters. The first paremeter is the filename and the second one is the file access mode. The default access mode is ```c``` which stand for opening an existing shelf or creating a new one if it doesn't exist. The alternative shelve access modes are:

* ```r``` is a read-only shelf.
* ```w``` is a read-wrtie shelf that *must* exist or an exception will be thrown.
* ```n``` is a new, empty shelf; any previous versions will be overwritten.

It is absolutely necessary to ensure that a shelf has been closed properly in order to make sure that the objects have been saved to a persistent disk. The shelf is not a contest manager itself but you can use the ```contextlib.closing()``` function in order to ensure the properer closing of a shelf.

This is what working with a shelf would look like:

```Python
import shelve
from contexltib import closing
from pathlib import Path

db_path = Path.cwd() / "data" / "database.db"
with closing(shelve.open(str(db_path))) as shelf:
    process(shelf)
```

We have opened a shelf and have provided the open shelf to some process that does the real work of our application. When this process is finished or if the process throws an exception, the context manager will ensure that the shelf will be closed properly.

## Designing keys for our objects.

The ```shelve``` and ```dbm``` modules provide immediate access to the objects that they store. This is done using a mapping-like structure. The ```shelve``` module stores its objects into a dictionary-like structure. It contains keys based on which you can retrieve your serialized objects and the objects are stored as values. The shelf mapping exists on persistent storage so that means that the objects that you are storing on a shelf will be immediately serialized and saved.

We must identify a shelf object with a unique key. Strings are very common data types used for keys. In our problem domain we can usually find a key that we can apply to an object. The key must be unique since a key can only point towards one object. This influences our class design since we must think about integrating those keys to our problem domain. In most cases we can add those keys as attributes to our objects. In the case where an object has its own key, we can add it on the shelf much easily using something like this: ```shelf[object.key] = object```. This is the simplest case and it also sets the pattern for more complex cases.

When our application doesn't find an appropriate key for an object we must build a so called *surrogate key*. That happens when we can't find a unique value from our object that can persist in time and that is unique. That value must be unique and is not allowed to change. This is when we must build a made-up value for our object so we can store it. It's just like a primary key in databases.

Objects might have certain candidates for primary keys. If an object has for example a ```datetime``` value we could use that as a primary key but that is not always the case where that is a valid value to use as a primary key. If an object has for example a ```datetime``` value we could use that as a primary key but that is not always the case where that is a valid value to use as a primary key

There is also the possibility of combining multiple values of our object in order to create a primary key. That would be called a **composite key**. This idea is however not valid in all problem domains since the key wouldn't be atomic anymore and any changes in the object's attributes that were used in order to build the composite key would lead to data update problems.

The simplest and most reliable way of building a key for a problem domain where the key can be unique and consistent and wouldn't lead to any data update problems would be to build a **surrogate key**. This key wouldn't have to depend on the data of the object, it would just be added to the object as a new attribute.

The string representation of such objects with *surrogate keys* when adding them to a shelf could follow the following design: ```class_name:oid``` ( where ```oid``` is object id; the surrogate key in case ). We should keep the ```class_name``` in our shelf key even if we only want to keep objects of certain types in persistent states just to ensure maintainability and to save a namespace for indexes and administrative metadata.

When adding an object to a shelf, it would look like this:

```shelf[f"{object.__class__.__name__}:{object.key}"] = object```

## Generating surrogate keys for objects

One way of generating surrogate keys is using an integer counter. In order to keep track of it, we can store the counter in our database along with the other objects.
Python has a method called ```id()``` that returns an integer that represents the address in memory of a certain object. That id however should never be used as an integer counter since it doesn't have any guarantees of any kind.

Since we are going to add some administrative object to our shelf we must give these objects some unique keys with a distinctive prefix in order to properly differentiate them from the other objects that we want to store. 
In our case we can use something like ```_DB```. This will be a class name used for all administrative objects. 
Administrative objects are objects that help us keep track of certain things in our database ( for example the index counter ) or objects in general that helps us administrate the objects that we store on the shelves.

We need to choose the granularity of storage:

* **Coarse-grained:** We can create a single ```dict``` object with all of the administrative overheads for surrogate key generattions. A single key, such as ```_DB:max```, can identify this object. Within this ``dict```, we could map class names to the maximum identifier values used. Every time we create a new object, we assign the ID from this mapping and then also replace the mapping in the shelf.
* **Fine-grained:** We can add many items to the database, each of which as the maximu key value for a different class of objects. Each of these additional key items has the form of ```_DB:max:class```. The value for each of these keys is just an integer, the largest sequential identifier assigned so far for a given class.

So, summarized, what we want to do is to store the surrogate key in our database in an administrative object that has the prefix key ```_DB```. Now, we have to options. We can either store a general surrogate key that will be used for all types of objects that we will store in our shelve which would be **coarse-grained storage**. The second option would be to store a surrogate key for each type of object that we are going to store in our database, that would be **fine-grained storage**.

## Designing a class with a simple key

It is very helpful to store the key for an object inside the object. That would it very easy to delete or replace the object inside the shelf.

When it comes to retrieving objects there are two use cases. The first use case is when we want to retrieve an object based on a certain key. The second use case is when we want to retrieve an object based on same values of its attributes, in which case we want have to get the keys of these objects through queries.

For every class that we create we can an attribute ```_id``` that will store the surrogate key for that object. 

Here is an example of how we can build a ```Blog``` class:

```Python
from dataclasses import dataclass, field
from Post import Post
from typing import List


@dataclass
class Blog:
    title: str
    entries: List[Post] = field(default_factory = list)
    underline: str = field(init=False, compare=False)

    # Part of the persistence, not essential to the class.
    _id: str = field(default="", init=False, compare=False)

    def __post_init__(self) -> None:
        self.underline = "=" * len(self.title)
```

This is how we could store this object on a shelf:

```Python
import shelve
from pathlib import Path

# Create the object
blog_object = Blog(title="Blog Title")

# Open the shelf 
path = str(Path.cwd() / "data" / "database.db")
shelf = shelve.open(path)

# Add a surrogate key to the object that we want to store
blog_object._id = "Blog:1"

# Save the object using the following format -> { shelf[object.key] = object }
shelf[blog_object._id] = blog_object
```

We have first opened the a shelf on a database ( i have chosen a sqlite database ). After opening the database, we have added the surrogate key to our object using the formatting that we've previously talked about and then we have saved the object to the shelf using the surrogate key.

We can also fetch the object from the shelf using the same exact surrogate key:

```Python
blog_saved = shelf["Blog:1"]
print(blog_saved.title) # Blog Title
shelf.close()
```

## Designing classes for containers or collections.

When it comes to storing complex objects like containers which are objects that contain other objects inside of them there are a couple of design strategies that we have to take a look at.
When we have a complex object, such as ```Blog```, we can persist the entire container as a single, complex object on our shelf. Storing large containers involves coarse-grained storage. If we change a contained object, the entire container must be serialized and stored since the container itself has been changed. 

## Referring to objects via foreign keys.

We have already talked about adding primary keys to our objects. When we have child objects that refer to parent object we have additional design decisions to make. One of the most important design decisions is thinking about how we will structure the primary keys of child objects. There are two common strategies for child keys:

* ***```"Child:cid"```:*** **We can use this when we have children taht can exist independently of an owning parent.** For example, an item on an invoice refers to a product; the product can exist even if there's no invoice item for the product.
* ***```"Parent:pid:Child:cid"```:*** **We can use this when the child cannote xist without a parent.** A customer address doesn't exist whtout a customer to contain the address in the first place. When the children are entirely dependent on the parent, the child's key can contain the owning parent's ID to reflect this depedency.

In our example with the ```Blog``` and ```Post``` class, a ```Post``` cannot exist without a ```Blog```, therefore we will have to implement the second design option. This is how a post would look like:

```Python
@dataclass
class Post:
    date: datetime.datetime
    title: str
    rst_text: str
    tags: List[str]
    underline: str = field(init=False)
    tag_text: str = field(init=False)

    # Part of the persistence, not essential for the class
    _id: str = field(default='', init=False, repr=False, compare=False)
    _blog_id: str = field(default='', init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.underline = "-" * len(self.title)
        self.tag_text = " ".join(self.tags)
```

This is how we would post objects to our shelf:

```Python
import shelve
from pathlib import Path

# Create the objects
first_post_object = Post(
    date = datetime.datetime(2013, 11, 14, 17, 25),
    title = "First Post Object Title",
    rst_text = """Rst Text""",
    tags = ("Tag1", "Tag2", "Tag3", "Tag4", "Tag5")
)
second_post_object = Post(
    date = datetime.datetime(2013, 11, 18, 15, 30),
    title = "Second Post Object Title",
    rst_text = """Rst Text""",
    tags = ("Tag1", "Tag2", "Tag3", "Tag4", "Tag5")
)

# Create the path to the database
path = str(Path.cwd() / "data" / "database.db")

# Open the shelf
shelf = shelve.open(path)

# Get the blog object
blog = shelf["Blog:1"]

# Assign the blog's primary key to the foreign key of the post so that we know to which blog the post belongs to
first_post_object._blog_id = blog._id
first_post_object._id = first_post_object._blog_id + ":Post:1"
shelf[first_post_object._id] = first_post_object

second_post_object._blog_id = blog._id
second_post_object._id = second_post_object._blog_id + ":Post:2"
shelf[second_post_object._id] = second_post_object

print(list(shelf.keys())) # ['Blog:1', 'Blog:1:Post:1', 'Blog:1:Post:2']
print(first_post_object._id) # 'Blog:1:Post:1'
print(first_post_object._blog_id) # 'Blog:1'
```

We have first created the post objects and then opened the shelf in order to get the blog object.
We have then assigned the blog object's primary key to the foreing key, which in our case is the blog id, to our posts. We have then saved the posts using their complete id which consisted of their post id and their foreign key ( the blog id ).

## Designing CRUD operations for complex objects

When we decompose collections into a number of independent objects we will have multiple classes of objects on the shelves. This leads of coures to a fine-grained designed storage. This also leads to seperate sets of CRUD operations for each class. In some cases, since the objects are independet, we can execute CRUD operations independently on certain objects without worrying about them having any impact on any other objects. 
In some relational databases, we have the so called *cascading* effect where if you delete for example the ```Blog``` object, all the other ```Post``` objects that were related to that ```Blog``` object will be deleted as well.

In our example, the ```Blog``` and the ```Post``` object have a relationship. The child object, ```Post``` can't exist without the parent object ```Blog```. When it comes to CRUD operations, this leads to the following considerations:

* Consider the following CRUD operations on independent objects:

    * We may create a new, empty parent, assigning a new primary key to this object. We can later assign children to this parent. Code such as ```shelf[f'parent:{object.id}'] = object``` creats a parent object in the shelf.
    * We may update or retrieve this parent without any effect on the children. We can perform ```shelf[f'parent:${object.id}']``` on the right side of the assignment to retrieve a parent. Once we have the object, we can perform ```shelf[f'parent:${object.id}'] = object``` to persist a change
    * Deleting the parent can lead to one of two behaviors. One choice is to cascade the deletion to include all the children that refer to the paretn. Alternatively, we may write code to prohibit the deletion of paretns that still have child references. both are sensible, and the choice is driven by the requirements imposed by the problem domain.

* Consider the following CRUD operations on dependent objects:

    * We may create a new child that refers to an existing parent. We must also decide what kind of keys we want to use for children and parents.
    * We can update, retrieve, or delete the child outside the parent. This can include assigning the child to a different parent.

## Searcing, scanning and querying

Searching, scanning and querying are synonyms, I'll use them interchangeably. 
Seraching can be very inefficient if we examine all the objects in a database and apply a filter on them. Working with a subset of items is a lot better.

When a child class has an independent-style key, we can scan a shelf for all instances of some ```Child``` class:

```Python
children = (
    shelf[key] for key in shelf.keys() if key.startswith("Child:")
)   
```

When a child has a dependent-style key, we can search for the children of a specific parent using more complex matching:

```Python
children_of = (
    shelf[key] for key in shelf.keys() if k.startswith(f"{parent}:Child:")
) 
```

When using the hierarchical design ```Parent:pid:Child:cid``` we have to be careful when separating parents from their children. With this part of the key, we can have object with keys that look like this: ```Parent:pid``` that only represent the object but we can also have objects that look like this: ```Parent:pid:Child:cid``` that represent a certain object and its children. We have three kinds of conditions that we'll often use for these brute-force searches:

* ```key.startswith(f"Parent:{pid}")```: Finds a union of parents and children; this isn't a common requirement.
* ```key.startswith(f"Parent:{pid}:Child:")```: Finds children of the given parent.
* ```key.startswith(f"Parent:{pid}:")``` and "```:Child:```" ```not in key```: Finds parents, excluding any children.

## Designing an access layer for shelve

We will look at how we can use the ```shelve``` module inside an application. We will look at parts of an application that edits and saves blog posts. 

**Withing an application tier, we'll distinguish between two layers:**:

* **Application processing:** Withing the application layer, objects are not persistent. **These classes will embody the behavior of the application as a whole.** These calsses respon to the user selection of commands, menu items, buttons, and other processing elements.
* **Problem domain data model:** These are the objects that will get written to a shelf. These objects embody the state of the application as a whole.

> The classes to define an independent ```Blog``` and ```Post``` will have to be modified so that we can process them separately in the shelf container. **We don't want to cdreate a single, large container object by turning ```Blog``` into a collection class.**

Withing the data tier, there might be a number of features, depending on the complexity of the data storage: We'll focus on these two features:

* **Access:** These components provide uniform access to the *problem domain objects*. *We'll focus on the access tier*. We'll define an ```Access``` class that provides access to the ```Blog``` and ```Post``` instances. It will also manage the keys to locate the ```Blog``` nad ```Post``` objects in the shelf.
* **Persistence:** The components serialize and write *problem domain objevcts* to the persistent storage. **This is the ```shelve``` module**. The Access tier will depend on this.

We will break the ```Acess`` class into three seperate pieces. Here's the first part, showing the file open and close operations:

```Python
import shelve
from pathlib import Path
from typing import cast, Dict, Iterator, Union
from Blog import Blog
from Post import Post


class Access:
    def __init__(self) -> None:
        self.database: shelve.Shelf = cast(shelve.Shelf, None)
        self.max: Dict[str, int] = {"Post": 0, "Blog": 0}

    def new(self, path: Path) -> None:
        self.database = shelve.Shelf = shelve.open(str(path), "n")
        self.max: Dict[str, int] = {"Post": 0, "Blog": 0}

        self.sync()

    def open(self, path: Path) -> None:
        self.database = shelve.open(str(path), "n")
        self.max = self.database["_DB:max"]

    def close(self) -> None:
        if self.database:
            self.database["_DB:max"] = self.max
            self.database.close()

        self.database = cast(shelve.Shelf, None)

    def sync(self) -> None:
        self.database["_DB:max"] = self.max
        self.database.sync()

    def quit(self) -> None:
        self.close()
```

When we initialize the ```Access``` class we create two properties, the ```database``` and the ```max``` dictionary that keeps track of fine-grained index counters.
If we choose to create a database using the ```Access.new()``` method, we will update the ```database``` property and set it to a new shelf that opens in a specific path. We will also use the ```Access.sync()``` method which syncs the database administrative class ```_DB```'s ```max``` property to our ```max``` property.
If we choose to open a database using ```Access.open()``` then we will update the ```database``` property to be an opened shelf of that database and we will also update our ```max``` property to match the ```max``` property of the database's administrative ```_DB``` class.
When closing the database using ```Access.close()``` we update the database's administrative ```_DB``` class ```max``` property with our ```max``` property and then we close it.
We will add the following methods in order to create and retrieve blog and post objects and also to update an delete posts from the database:

```Python
    def create_blog(self, blog: Blog) -> Blog:
        self.max["Blog"] += 1
        key = f"Blog:{self.max['Blog']}"
        blog._id = key

        ###################################
        self.database[blog._id] = blog
        ###################################

        return blog

    def retrieve_blog(self, key: str) -> Blog:
        return self.database[key]

    def create_post(self, blog: Blog, post: Post) -> Post:
        self.max["Post"] += 1
        post_key = f"Post:{self.max['Post']}"
        post._id = post_key
        post._blog_id = blog._id

        #################################
        self.database[post._id] = post
        #################################

        return post

    def retrieve_post(self, key: str) -> Post:
        return self.database[key]

    def update_post(self, post: Post) -> Post:
        self.database[post._id] = post
        return post

    def delete_post(self, post: Post) -> None:
        del self.database[post._id]
```

When creating a new blog using the ```Access.create_blog()``` method we increment the Blog's index counter inside our ```max``` property and then give it a key using the ```f"Blog:{self.max["Blog"]"}``` format. Afterwards we add the blog inside our shelf using the key.
When creating a new post using ```Access.create_post()``` we also need the blog as an argument that the post can make a reference to. The post's counter will be incremented inside the ```max``` property. We will first add the post key using the same format that we've used with the ```Blog``` class: ```f"Post:{self.max['Post']}"``` and then we will add the blog id to the ```_blog_id``` property of the ```Post``` object. Then we will add the post to the shelf using its key.
When retrieving ```Blog``` or ```Post``` object we will use their key and return the object from the shelf using the given key. The same concept goes for updating and deleting ```Post``` objects, we just use the given key.

We can also add some iterators to our ```Access``` class:

```Python
    def __iter__(self) -> Iterator[Union[Blog, Post]]:
        for k in self.database:
            if k[0] == "_":
                continue  # Skip the administrative objects
            yield self.database[k]

    def blog_iter(self) -> Iterator[Blog]:
        for k in self.database:
            if k.startswith("Blog:"):
                yield self.database[k]

    def post_iter(self, blog: Blog) -> Iterator[Post]:
        for k in self.database:
            if k.startswith("Post:"):
                if self.database[k]._blog_id == blog._id:
                    yield self.database[k]

    def post_title_iter(self, blog: Blog, title: str) -> Iterator[Post]:
        return (p for p in self.post_iter(blog) if p.title == title)
```

## Creating indexes to improve efficiency

One of the rules of efficiency is to completely avoid search. The use of search is the **definition of an inefficient application**. Brute-force search is perhaps the worst possible way to work with data.

In order to avoid search and make our application more efficient we will make use of indexes which will store the items that users are more likely to want.

Example of indexing in our ```Access``` class:

```Python
class IndexedAccess(Access):
    def create_post(self, blog: Blog, post: Post) -> Post:
        super().create_post(blog, post)
        # Update the index; append doesn't work.
        blog_index = f"_Index:{blog._id}"
        self.database.setdefault(blog_index, [])
        self.database[blog_index] = self.database[blog_index] + [post._id]

        return post

    def delete_post(self, post: Post) -> None:
        super().delete_post(post)

        # Update the index.
        index_list = self.database[post._blog_id]
        index_list.remove(post._id)
        self.database[post._blog_id] = index_list

    def post_iter(self, blog: Blog) -> Iterator[Post]:
        blog_index = f"_Index:{blog._id}"
        for k in self.database[blog_index]:
            yield self.database[k]
```

We have now indexed our posts. When creating a new post we add it's id in the ```blog_index``` key of the database which is an administrative object.

## Design considerations and tradeoffs

One of the strenghts of ```shelve``` is that we can persist distinct items very easily. This also comes with a lot of responsabilty since it imposes a design burdern to identify the proper granularity. 

> Too fine a granularity and we waste time assembling a container object from pieces scattered through the database. Too coarse a granularity, and we waste time fetching and storing items that aren't relevant.

Since a shelf requires a key we must design appropriate keys for our objects and also manage them properly.

## Application software layers

Because of the sophistication available and freedom when using ```shelve`` our application needs a proper architecture, that means that it must be properly layered. Generally, we'll look at software architectures with layers such as the following:

* **Presentation layer:** The top-level user interface, either a web presentation or a desktop GUI.
* **Application layer:** This internal services or controllers that make the application work .This could be called the processing model, which is different from the logical data model.
* **Bussiness layer or problem domain model layer:** The objects that define the business domain or problem space. This is sometimes called the logical data model.
* **Infrastructure aspects:** Some applications include a number of cross-cutting concerns or aspects such as logging, security, network access or transaction management. These tend to  be pervasive and cut across multiple layers.
* **Data access layer:** These are protocols or methods to access data objects.
* **Persistence layer:** This is the physical data model as seen in file storage.

# 12. Storing and Retrieving Objects via SQLite

## SQL databases, persistence, and objects

When using with SQLite our application works with an implicit access layer that is based on the SQL language. It's structure using rows and columns that is very different from our way of thinking in OOP is known as an **impedance mismatch**.
Withing SQL databases there are three tiers of data modeling:

* **The conceptual model:** These are entities and relationships inside of the SQL model. They are not tables or columns, they might however represent views on tables. In most cases, the conceptual model can map to Python objects. This is the place where an **Object-Relational Mapping (ORM)** layer is useful.
* **The logical model:** These are the tables, rows and columns that appear in the SQL database
* **The physical model:** These are the files, blocks, pages, bits, and bytes of persistence physical storage.

As previously mentioned, the fact that the structure of SQL using columsn, rows, tables, etc. doesn't perfectly match the idea of how we build and structure our code in OOP is called an **impedance mismatch**. One of the most important design decisions to take is how to cover it.
Here are three strategies:

* **Minimal mapping to Python:** This means that we won't map rows to python objects and that the application will work entirely within the SQL framework. This, however, limits us to the data types used in SQL.
* **Manual mapping to Python:** We can define an access layer that maps the application's class definitions to the SQL logical model ( tables, columns, rows, keyl, etc. ). This works as a bridge between our application and SQL.
* **ORM layer:** We can use an ORM layer in order to map python objects and the SQL logical model.


## The SQL data model - rows and tables

SQL only has a few atomic data types. An instance of an atomic data type is a single, indivisible unit of data. Each row essentially defines an object and the properties and defined by the columns. A table is the single data-structure that can be met in SQL and is essentially just a list of rows, where rows represent objects. 
We can also select a column to represent the primary key so we can look at the rows as a mapping between the key and the rest of the object. We can actually just implement the key in our code as well in order to identify an object by its key and to make mapping objects between python and SQL rows easier.

As previously mentioned, rows represent objects. That also means that each row can represent a mutable ```@dataclass```. Tables will then represent lsits of individual ```@dataclass``` objects:

```Python
from dataclasses import dataclass
from typing import Union, Text
import datetime
SQLType = Union[Text, int, float, datetime.datetime, datetime.date, bytes]


@dataclass
class Row:
    column_x: SQLType
    ...


Table = Union[List[Row], Dict[SQLType, Row]]
```


The SQL language can be partitioned into three sublanguages: 

* the ***data definition language (DDL)***
* the ***data manipulation language (DML)***
* the ***data control language (DCL)***


Here is an exmaple for DDL:

```SQL
CREATE TABLE blog(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT
);
CREATE TABLE post(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TIMESTAMP,
    title TEXT,
    rst_text TEXT,
    blog_id INTEGER REFERENCE blog(id)
);
CREATE TABLE tag(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phrase TEXT UNIQUE ON CONFLICT ALL
);
CREATE TABLE assoc_post_tag(
    post_id INTEGER REFERENCE post(id),
    tag_id INTEGER REFERENCE tag(id),
);
```

In order to build the tables using python:

```Python
import sqlite3
database = sqlite3.connect("database.db")
database.executescript(sql_ddl)
```

First we have create a connection to our database using the ```connect()``` method and that we have executed the script for the creation of the tables using ```executescript()```. We can also build a cursor using the ```database``` object with ```database.cursor()``` in order to execute scripts whenever we want.

## CRUD processing via SQL DML statements

The followin CRUD operations map directly to the SQL language statments:

* Creation via ```INSERT```
* Retrieval via ```SELECTj```
* Update via ```UPDATE```
* Deletion via  ```DELETE```

However, building SQL statements using string manipulation involves security concerns ( see http://xkcd.com/327/ )

***Never build literal SQL DML statements with string manipulation. It is very high risk to attempt to sanitize user-supplied text.***

Python offers a work-around when it comes to string mainpulation. You can use positional binding with ```?``` or named bindings with ```:name``` in order to safely build SQL statements.

***Here is an example using positional bindings:***

```Python
create_blog = """
    INSERT INTO BLOG(title) VALUES(?)
"""
with closing(database.cursor()) as cursor:
    cursor.execute(create_blog, ("Travel Blog", ))

database.commit()
```

In this example we have used positional bindings with ```?``` in order to safely build an ```INSERT``` statement. We have also used a ```cursor``` object in order to execute the statement after binding a tuple of values. The final commit makes this change persistent, releasing any locks that were held.

> In some applications, the SQL is stored as a sepearate configuration item. Keeping SQL separate is best handled as a mapping from a statement name to the SQL text. This can simplify application maintenance by keeping the SQL out of the Python programming.

Now here is an exmample

***Here is an example using named bindings:***

```Python
update_blog = """
    UPDATE blog SET title=:new_title WHERE title=:old_title
"""

with closing(database.cursor()) as cursor:
    cursor.execute(
        update_blog,
        dict(
            new_title = "2013-2014 Travel",
            old_title="Travel Blog"
        )
    )


database.commit()
```

In this ```UPDATE``` statement we have used named bindings. Named bindings allow us to map names to certain values using dictionaries. 
When python goes over the SQL statement, it will safely map the values in the dictionary to the SQL statement.

## Querying rows with the SQL SELECT statement

When it comes to querying rows, the ```SELECT``` statement is very helpful. Here is an example:

```Python
query_blog_by_title = """
    SELECT * FROM blog WHERE title=?
"""

with closing(database.cursor()) as cursor:
    cursor.execute(query_blog_by_title, ("2013-2014 Travel", ))

    for blog in cursor.fetchall():
        print("Blog {0}".format(blog))
```

After executing a ```SELECT``` statement, we have to get the values using a the ```fetchall()``` method ( there are ```fetch```-like methods)


## SQL transactions and the ACID properties

All the SQL DML statements operatin withing the context of a SQL transaction. A transaction must be commited as whole and rolled back as whole. This supports the atomicity property by creating a signle, atomic, indivisible change from one consistent state of the database to the next consistent state.

***SQL DDL statements ( i.e. ```CREATE```, ```DROP```, etc. ) do not work withing a transaction. They implicitly end any previous in-process transactions.*** That happens because the statements change the structure of the database, so it wouldn't make sense for other transactions to use a state of the database that is no longer valid. This is why they are termianted.

> Unless working in a special ***read uncommitted*** mode, each connection to the cadtaabase sees a consistent version of the data containin only the reuslts of the committed transactions. Uncommitted trasactions are generaly indivisible to other database client processes, supporintg the consistency property.

A SQL transaction also supports an isolation level. An isolation level describes how the SQL DML statements will interefact among multiple, concurrent processes.

Here are the following 4 isolation levels:

* ***```isolation_level=None```:*** This is the default, otherwise known as the **autocommit** mode. In this mode, each inddividual SQL statement is committed to the database as it's executed. This can break the atomicity of complex transactions.
* ***```isolation_level='DEFERRED'```:*** In this mode, locks are acquired late in the transaction. The ```BEGIN``` statement, for exampe, does not immediately acquire any locks. Other read operations ( i.e ```SELECT``` ) will acquire shared locks. Write operations will acquire reserved locks. While this can maximize the concurrency, it can also lead to deadlocks among competing trasaction processes.
* ***```isolation_level='IMMEDIATE'```:*** In this mode, the transaction ```BEGIN``` statement acquires a lock that prevents all writes. Reads, however, will continue normally. This avoid deadlocks, and works well when transactions can be completed quickly.
* ***```isolation_level='EXCLUSIVE'```:*** In this mode, the transaction ```BEGIN``` statement acquires a lock that prevents all access except for connections in a special read uncommitted mode.

In SQL you have to use ```BEGIN TRANSACTION```, ```COMMIT TRANSACTION``` and ```ROLLBACK TRANSACTION``` in order to bracket a changes together. In Python, things are simplified. You just have to use the ```BEGIN``` statement in order to begin a transaction. The rest of the statements are taken care of by the ```sqlite3.Connection``` object when using methods such as ```commit()``` or ```rollback()```.

Example:

```Python
database = sqlite3.connect("database.db", isolation_level='DEFERRED')

try:
    with closing(database.cursor()) as cursor:
        cursor.execute("BEGIN")
        # cursor.execute("STATEMENT 1")
        # cursor.execute("STATEMENT 2")

    database.commit()
except Exception as e:
    database.rollback()
```

In this example we have created a deferred connection to the database. This leads to the requirement to explicitly being and end each transaction. One typical scenario is to wrap a relevant DML statement in a ```try``` block and commit it and if the transaction goes bad use the ```except``` statement to do a rollback.
You can also use a context manager for this:

```Python
database = sqlite3.connect("database.db", isolation_level='DEFERRED')

with database:
    database.execute("STATEMENT 1")
    database.execute("STATEMENT 2")
```

## Designing primary and foregin databas ekeys

There are three design patterns for relationships:

* ***One-to-many:*** A number of children belong to a single parent object. Analog to our previous examples, is the relationship between one parent blog and many child posts. The ```REFERENCES``` clause shows us that many rows in the ```post``` table will reference one rwo from the ```blog``` table.
* ***Many-to-many:*** This relationship is between many posts and many tags. This requires an intermediate association table betwen the ```post``` and ```tag``` tables; the intermediate tables has two (or more) foreign key associations. The many-to-many association table can also have attributes of its own.
* ***One-to-one:*** This relationship is a less common design pattern. There's no technical difference from a one-to-many relationship. This is a question of the cardinality of rows on the child side of the relationship. To enforce a one-to-one relationship, some processing must prevent the creation of additional children.

The table relationships can be implemented in the database in either or both of the following ways:

* **Explicit:** We could call these declared, as they're part of the DDL declaration for a database. Ideally, they're enforced by the database server, and failure to comply with the relationship's constraints can lead to an error of some kind. These relationships will also be repeated in queries.
* **Implicit:** These are relationships that are stated only in queries; they are not a formal part of the DDL.

## Mapping Python objects to SQLite BLOB columns

SQLite includes a BLOB ( binary large object ) data type. We can pickle our objects inside a column of this type. This technique however has a great impact on SQL processing since DML statements cannot be used on BLOB types.
This technique should however only be used with media types such as images, videos, etc. since in those cases it is acceptable for those objects to be opaque to the surrounding SQL processing.

## Mapping Python objects to database rows manually

We can map SQL rows to class definitions so that we can create proper Python object instances from the data in a database.

## Adding an ORM layer

