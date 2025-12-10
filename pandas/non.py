
import pandas as pd
from caas_jupyter_tools import display_dataframe_to_user

# Fixing the mismatch in lengths between Category and Work Name
# Count of work names = 59, so we need 59 categories

categories = (
    ["Home-Based Crafts & Handwork"] * 16 +
    ["Food-Related Work"] * 8 +
    ["Farming / Gardening / Eco-Based Work"] * 4 +
    ["Digital and Passive Skills"] * 11 +
    ["Beauty & Event Services"] * 3 +
    ["Wellness & Education"] * 3 +
    ["Pet-Related Work"] * 2 +
    ["New Extra Suggestions"] * 12  # Adjusted to make total = 59
)

work_names = [
    "Tailoring / Sewing",
    "Handicrafts (knitting, beadwork, etc.)",
    "Embroidery Work",
    "Hand Embroidery",
    "Pote/Mala Making",
    "Cloth Bag Making",
    "Paper Bag Making",
    "Knitting and Crocheting",
    "Jewelry Making",
    "Traditional Broom Making",
    "Bamboo Crafting",
    "Traditional Sculpture",
    "Pottery",
    "Candle Making",
    "Soap Making",
    "Agarbatti Making",
    "Pickle Making and Selling",
    "Fish Pickle Making and Selling",
    "Homemade Snacks and Food Delivery",
    "Catering Service (small scale)",
    "Baking and Cake Decoration",
    "Jam, Jelly and Sauce Production",
    "Nepali Food Recipe Content Creation",
    "Vegetable Farming",
    "Mushroom Farming",
    "Indoor Plant Selling / Kitchen Garden Setup",
    "Organic Compost Production",
    "Content Writing",
    "Digital Marketing",
    "Web Development",
    "Graphic Design",
    "Photography",
    "Bookkeeping / Accounting",
    "Data Entry Operator",
    "Nepali Recipe Blog / YouTube Channel",
    "Affiliate Marketing / Blogging",
    "Online Course Creation",
    "Virtual Assistant Services",
    "Makeup Artist",
    "Beauty Parlor Service",
    "Event Planning",
    "Yoga / Meditation Instructor",
    "Home Tuition / Child Care",
    "Spoken English / Basic Computer Classes at Home",
    "Pet Sitting / Dog Walking",
    "Pet Food Production (home-based)",
    "Sewing Uniforms for Schools",
    "Customized Apron / Baby Bib Making",
    "Recycling Old Clothes to Make New Products",
    "Tiffin Service for Office-goers near you",
    "Second-Hand Book Rental for School Kids",
    "Homemade Toys or Fabric Dolls",
    "YouTube Voiceover for Kids’ Stories",
    "Sell Products via Facebook / TikTok Live",
    "Freelance Translator (English-Nepali)",
    "Customized Gift Hamper Creation",
    "Making Decorative Diyas, Rakhis, or Festival Items",
    "Micro-Green Farming or Herbal Garden Kit Making",
    "WhatsApp-Based Home Business Catalog"
]

# Create the corrected DataFrame
df_corrected = pd.DataFrame({
    "Category": categories,
    "Work Name": work_names
})

# Display to user
display_dataframe_to_user(name="Work Ideas for Married Women", dataframe=df_corrected)
