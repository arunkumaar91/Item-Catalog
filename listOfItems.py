from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, ListItems

engine = create_engine('sqlite:///itemcatalog.db')

# DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

# Create user
userOne = User(
    name="Arunkumaar Saravanen",
    email="arunkumaar91@udacity.com",
    picture='https://d125fmws0bore1.cloudfront.net/assets/udacity_share-317a7f82552763598a5c91e1550b7cd83663ce02d6d475d703e25a873cd3b574.png')
session.add(userOne)
session.commit()

"""userTwo = User(name="Robert Johnah", email="robjoh@udacity.com",
             picture='https://1onjea25cyhx3uvxgs4vu325-wpengine.netdna-ssl.com/wp-content/themes/udacity_wp_1_8/images/Udacity_Logo_SVG_200x35.svg')
session.add(userOne)
session.commit()"""

# List of Categories and Items

# Category 1 - Electronics
category1 = Category(user_id=1, name="Electronics")
session.add(category1)
session.commit()

# Items in Category 1
categoryItem1 = ListItems(
    user_id=1,
    name="TV",
    description="A television, commonly referred to as TV, telly or the tube, is a telecommunication medium used for transmitting sound with moving images in monochrome (black-and-white), or in colour, and in two or three dimensions",
    price="$700",
    subcategory="HouseHold",
    category=category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = ListItems(
    user_id=1,
    name="Cellphones",
    description="A telephone with access to a cellular radio system so it can be used over a wide area, without a physical connection to a network.",
    price="$700",
    subcategory="HouseHold",
    category=category1)
session.add(categoryItem2)
session.commit()


# Category 2 - Furniture
category2 = Category(user_id=1, name="Furniture")
session.add(category2)
session.commit()

# Items in Category 2
categoryItem1 = ListItems(
    user_id=1,
    name="Dining Table",
    description="The dining room table, which is used for seated persons to eat meals",
    price="$1500",
    subcategory="HouseHold",
    category=category2)
session.add(categoryItem1)
session.commit()

categoryItem2 = ListItems(
    user_id=1,
    name="TV Stands",
    description="To withstand the TV",
    price="$150",
    subcategory="HouseHold",
    category=category2)
session.add(categoryItem2)
session.commit()


# Category 3 - Clothing
category1 = Category(user_id=1, name="Clothing")
session.add(category1)
session.commit()

# Items in Category 3
categoryItem1 = ListItems(
    user_id=1,
    name="Shirts",
    description="A shirt is more specifically a garment with a collar, sleeves with cuffs, and a full vertical opening with buttons or snaps",
    price="$40",
    subcategory="Apparels",
    category=category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = ListItems(
    user_id=1,
    name="Pants",
    description="Trousers or pants are an item of clothing worn from the waist to the ankles, covering both legs separately",
    price="$25",
    subcategory="Apparels",
    category=category1)
session.add(categoryItem2)
session.commit()


# Category 4 - Shoes
category1 = Category(user_id=1, name="Shoes")
session.add(category1)
session.commit()

# Items in Category 4
categoryItem1 = ListItems(
    user_id=1,
    name="Casual Shoes",
    description="Used for casual occasions",
    price="$70",
    subcategory="Apparels",
    category=category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = ListItems(
    user_id=1,
    name="Athletic Shoes",
    description="For sports purposes",
    price="$120",
    subcategory="Apparels",
    category=category1)
session.add(categoryItem2)
session.commit()


# Category 5 - Toys
category1 = Category(user_id=1, name="Toys")
session.add(category1)
session.commit()

# Items in Category 5
categoryItem1 = ListItems(
    user_id=1,
    name="Action Figures",
    description="An action figure is a poseable character figurine, made of plastic or other materials, and often",
    price="$10",
    subcategory="Baby Care",
    category=category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = ListItems(
    user_id=1,
    name="Dolls",
    description="A doll is a model of a human being, often used as a toy for children",
    price="$30",
    subcategory="Baby Care",
    category=category1)
session.add(categoryItem2)
session.commit()


# Category 6 - Video Games
category1 = Category(user_id=1, name="Video Games")
session.add(category1)
session.commit()

# Items in Category 6
categoryItem1 = ListItems(
    user_id=1,
    name="Virtual Reality",
    description="the computer-generated simulation of a three-dimensional image or environment that can be interacted with in a seemingly real or physical way by a person using special electronic equipment, such as a helmet with a screen inside or gloves fitted with sensors.",
    price="$399",
    subcategory="Gaming",
    category=category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = ListItems(
    user_id=1,
    name="PlayStation",
    description="The PlayStation is a home video game console",
    price="299",
    subcategory="Gaming",
    category=category1)
session.add(categoryItem2)
session.commit()


# Category 7 - Sports
category1 = Category(user_id=1, name="Sports")
session.add(category1)
session.commit()

# Items in Category 7
categoryItem1 = ListItems(
    user_id=1,
    name="Cricket Bat",
    description="A cricket bat is a specialised piece of equipment used by batsmen in the sport of cricket to hit the ball, typically consisting of a cane handle attached to a flat-fronted willow-wood blade.",
    price="$130",
    subcategory="Gaming",
    category=category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = ListItems(
    user_id=1,
    name="Soccer Ball",
    description="A football, soccer ball, or association football ball is the ball used in the sport of association football",
    price="$25",
    subcategory="Gaming",
    category=category1)
session.add(categoryItem2)
session.commit()

print "Added the List of Items!!!"
