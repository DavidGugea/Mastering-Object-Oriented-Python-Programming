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

