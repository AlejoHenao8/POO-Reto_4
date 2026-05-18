# BASE CLASS

class MenuItem:
    """
    Base class that represents any item on the restaurant menu.
    Every menu item has a name and a price. Subclasses can
    override total_price() to add custom pricing logic
    (e.g. tax, surcharge).
    """

    def __init__(self, name, price):
        """
        Constructor: stores the item name and unit price.

        Parameters:
            name (str):   display name of the item.
            price (float): base price before any adjustments.
        """
        self._name = name
        self._price = price  # base unit price

    # --- Getters / Setters (base attributes) ---

    @property # El @ es idea de la IA
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("name must be a non-empty string.")
        self._name = value.strip()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("price must be a non-negative number.")
        self._price = float(value)

    def total_price(self):
        """
        Returns the final price for this item.
        Subclasses override this to add surcharges or
        apply category-specific rules.
        """
        return self._price

    def description(self):
        """
        Returns a short human-readable description of the item.
        Subclasses override this to include their extra attributes.
        """
        return f"{self._name} — ${self._price:.2f}"


# SUBCLASS 1: Beverage

class Beverage(MenuItem):
    """
    Represents a drink. Adds two beverage-specific attributes:
      - is_alcoholic: bool — used for discount logic in Order.
      - mls: int           — serving size (informational).

    Alcoholic beverages carry a 10% sin tax on top of the
    base price.
    """

    def __init__(self, name, price, is_alcoholic, mls):
        super().__init__(name, price)
        self._is_alcoholic = is_alcoholic
        self._mls = mls

    # --- Getters / Setters ---

    @property
    def is_alcoholic(self):
        return self._is_alcoholic

    @is_alcoholic.setter
    def is_alcoholic(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_alcoholic must be a boolean.")
        self._is_alcoholic = value

    @property
    def mls(self):
        return self._mls

    @mls.setter
    def mls(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("mls must be a positive integer.")
        self._mls = value

    def total_price(self):
        """
        Alcoholic drinks get a 10% sin tax added.
        Non-alcoholic drinks return the base price.
        """
        if self._is_alcoholic:
            return self._price * 1.10
        return self._price

    def description(self):
        drink_type = "alcoholic" if self._is_alcoholic else "non-alcoholic"
        return (
            f"[Beverage] {self._name} ({self._mls}ml, {drink_type})"
            f" — ${self.total_price():.2f}"
        )

# SUBCLASS 2: Appetizer

class Appetizer(MenuItem):
    """
    Represents a starter dish. Extra attributes:
      - is_vegan: bool   — for dietary info.
      - portion: str     — e.g. "individual", "to share".

    Shareable appetizers ('to share') get a 15% upcharge
    because they use larger portions.
    """

    def __init__(self, name, price, is_vegan, portion):
        super().__init__(name, price)
        self._is_vegan = is_vegan
        self._portion = portion  # "individual" | "to share"

    # --- Getters / Setters ---

    @property
    def is_vegan(self):
        return self._is_vegan

    @is_vegan.setter
    def is_vegan(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_vegan must be a boolean.")
        self._is_vegan = value

    @property
    def portion(self):
        return self._portion

    @portion.setter
    def portion(self, value):
        allowed = {"individual", "to share"}
        if value not in allowed:
            raise ValueError(f"portion must be one of {allowed}.")
        self._portion = value

    def total_price(self):
        """
        Shareable appetizers cost 15% more than the base price
        because they're larger portions.
        """
        if self._portion == "to share":
            return self._price * 1.15
        return self._price

    def description(self):
        diet = "vegetarian" if self._is_vegan else "non-veg"
        return (
            f"[Appetizer] {self._name} ({self._portion}, {diet})"
            f" — ${self.total_price():.2f}"
        )


# SUBCLASS 3: MainCourse

class MainCourse(MenuItem):
    """
    Represents a main dish. Extra attributes:
      - protein: str        — type of protein (chicken, beef…).
      - has_garnish: bool   — whether a side dish is included.

    Dishes that include a side dish get $2.50 added to
    the base price (side costs reflected transparently).
    """

    def __init__(self, name, price, protein, has_garnish):
        super().__init__(name, price)
        self._protein = protein
        self._has_garnish = has_garnish

    # --- Getters / Setters ---

    @property
    def protein(self):
        return self._protein

    @protein.setter
    def protein(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("protein must be a non-empty string.")
        self._protein = value.strip()

    @property
    def has_garnish(self):
        return self._has_garnish

    @has_garnish.setter
    def has_garnish(self, value):
        if not isinstance(value, bool):
            raise ValueError("has_garnish must be a boolean.")
        self._has_garnish = value

    def total_price(self):
        """
        Add $2.50 for side dishes that are included.
        """
        cost_garnish = 2.50 if self._has_garnish else 0
        return self._price + cost_garnish

    def description(self):
        garnish = "with side" if self._has_garnish else "no side"
        return (
            f"[Main] {self._name} ({self._protein}, {garnish})"
            f" — ${self.total_price():.2f}"
        )


# ORDER CLASS

class Order:
    """
    Represents a customer's order for one table.
    Holds a list of MenuItem objects.

    Composition-based discount rules (applied in total()):

    Rule 1: ≥ 1 MainCourse  → 10% off non-alcoholic drinks
    Rule 2: ≥ 2 MainCourses → 15% off all appetizers
    Rule 3: ≥ 2 alcoholic   → $1.00 off each alcoholic

    Discounts are computed here so item classes stay clean.
    """

    def __init__(self, table_number):
        self.table_number = table_number
        self.items = []

    def add_item(self, item):
        if not isinstance(item, MenuItem):
            print(f"Error: '{item}' is not a valid menu item.")
            return
        self.items.append(item)
        print(f"  Added: {item.name}")

    # --- Private helpers ---

    def _count_main_courses(self):
        """Counts MainCourse items in the order."""
        return sum(1 for item in self.items if isinstance(item, MainCourse))

    def _count_alcoholic_beverages(self):
        """Counts alcoholic Beverage items in the order."""
        return sum(
            1 for item in self.items
            if isinstance(item, Beverage) and item.is_alcoholic
        )

    def _compute_discounts(self):
        """
        Returns a dict that maps each item  to its discount amount,
        plus list of applied discount lines for the bill.
        """
        discounts = {}      # item_id -> discount amount
        applied = []        # list of human-readable discount notes

        n_mains    = self._count_main_courses()
        n_alcoholic = self._count_alcoholic_beverages()

        for item in self.items:
            discount = 0.0

            # Rule 1: ≥ 1 main course → 10% off non-alcoholic beverages
            if (n_mains >= 1
                    and isinstance(item, Beverage)
                    and not item.is_alcoholic):
                discount += item.total_price() * 0.10

            # Rule 2: ≥ 2 main courses → 15% off appetizers
            if n_mains >= 2 and isinstance(item, Appetizer):
                discount += item.total_price() * 0.15

            # Rule 3: ≥ 2 alcoholic beverages → $1.00 off each alcoholic drink
            if (n_alcoholic >= 2
                    and isinstance(item, Beverage)
                    and item.is_alcoholic):
                discount += 1.00

            if discount > 0:
                discounts[id(item)] = discount

        # Build summary lines (one per rule that triggered)
        if n_mains >= 1:
            affected = [
                item for item in self.items
                if isinstance(item, Beverage) and not item.is_alcoholic
            ]
            if affected:
                saved = sum(discounts.get(id(i), 0) for i in affected)
                applied.append(
                    f"  [Rule 1] Main course ordered → 10% off non-alcoholic"
                    f" beverages  -${saved:.2f}"
                )

        if n_mains >= 2:
            affected = [item for item in self.items if isinstance(item, Appetizer)]
            if affected:
                saved = sum(discounts.get(id(i), 0) for i in affected)
                applied.append(
                    f"  [Rule 2] 2+ main courses → 15% off appetizers"
                    f"  -${saved:.2f}"
                )

        if n_alcoholic >= 2:
            affected = [
                item for item in self.items
                if isinstance(item, Beverage) and item.is_alcoholic
            ]
            if affected:
                saved = sum(discounts.get(id(i), 0) for i in affected)
                applied.append(
                    f"  [Rule 3] 2+ alcoholic drinks → $1.00 off each"
                    f"  -${saved:.2f}"
                )

        return discounts, applied

    def total(self):
        """
        Calculates the bill by summing total_price() for each item,
        then applying composition-based discounts.

        Returns:
            float: final amount to pay.
        """
        subtotal   = sum(item.total_price() for item in self.items)
        discounts, _ = self._compute_discounts()
        total_discount = sum(discounts.values())
        return subtotal - total_discount

    def show_bill(self):
        """
        Prints the full itemized bill to the console,
        including applied discounts and the final total.
        """
        print("\n" + "=" * 55)
        print(f"  TABLE {self.table_number} — BILL")
        print("=" * 55)

        if not self.items:
            print("  No items ordered yet.")
            return

        # Print each item at its base (pre-discount) price
        subtotal = 0.0
        for item in self.items:
            print(f"  {item.description()}")
            subtotal += item.total_price()

        # Print subtotal
        print("-" * 55)
        print(f"  {'Subtotal':44s} ${subtotal:.2f}")

        # Print discounts (if any)
        discounts, applied_lines = self._compute_discounts()
        if applied_lines:
            print()
            print("  DISCOUNTS:")
            for line in applied_lines:
                print(line)

        # Print final total
        print("-" * 55)
        total_discount = sum(discounts.values())
        total = subtotal - total_discount
        print(f"  {'TOTAL':44s} ${total:.2f}")
        print("=" * 55)


# -------------------------------------------------------
# MENU — (used as the restaurant's catalog)
# -------------------------------------------------------

def build_menu():
    """
    Creates and returns a dictionary with all available
    menu items grouped by category.
    """
    menu = {
        # --- Beverages ---
        "mineral_water":    Beverage("Sparkling water",      2.50, False, 500),
        "lemonade":         Beverage("Lemonade",             3.80, False, 400),
        "craft_beer":       Beverage("Craft beer",           6.50, True,  330),
        "red_wine_glass":   Beverage("Red wine (glass)",     8.00, True,  150),

        # --- Appetizers ---
        "ceviche":          Appetizer("Ceviche",             9.50, False, "individual"),
        "cheese_board":     Appetizer("Cheese board",       14.00, True,  "to share"),
        "calamari":         Appetizer("Fried calamari",     10.50, False, "to share"),

        # --- Main courses ---
        "salmon_grill":     MainCourse("Grilled salmon",    22.00, "fish",    True),
        "beef":             MainCourse("Beef tenderloin",   28.00, "beef",    True),
        "chicken_marsala":  MainCourse("Chicken marsala",   18.50, "chicken", True),
        "risotto_funghi":   MainCourse("Mushroom risotto",  16.00, "none",    False),
        "pasta_carbonara":  MainCourse("Pasta carbonara",   15.50, "pork",    False),
    }
    return menu

# -------------------------------------------------------
# Tests
# -------------------------------------------------------

menu = build_menu()

# ----- Order 1: 3 mains + 2 alcoholic → all 3 discount rules fire
print("\n>>> Building order for table 4...")
table_order4 = Order(table_number=4)
table_order4.add_item(menu["craft_beer"])       # alcoholic   (Rule 1 + Rule 3)
table_order4.add_item(menu["red_wine_glass"])   # alcoholic   (Rule 1 + Rule 3)
table_order4.add_item(menu["cheese_board"])     # appetizer   (Rule 2)
table_order4.add_item(menu["salmon_grill"])     # main
table_order4.add_item(menu["beef"])             # main
table_order4.add_item(menu["chicken_marsala"])  # main
table_order4.show_bill()

# ----- Order 2: 1 main + no alcoholic → only Rule 1 (non-alc discount) fires
print("\n>>> Building order for table 2...")
table_order2 = Order(table_number=2)
table_order2.add_item(menu["lemonade"])         # non-alcoholic (Rule 1)
table_order2.add_item(menu["ceviche"])          # appetizer (no discount — only 1 main)
table_order2.add_item(menu["risotto_funghi"])   # main
table_order2.show_bill()

# ----- Order 3: 1 main + 2 alcoholic → Rule 1 (alc drinks, no effect) + Rule 3
print("\n>>> Building order for table 7...")
table_order7 = Order(table_number=7)
table_order7.add_item(menu["craft_beer"])       # alcoholic (Rule 3)
table_order7.add_item(menu["red_wine_glass"])   # alcoholic (Rule 3)
table_order7.add_item(menu["calamari"])         # appetizer (no discount — only 1 main)
table_order7.add_item(menu["pasta_carbonara"])  # main
table_order7.show_bill()