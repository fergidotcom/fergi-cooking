# Quick Reference Card

## 🚀 START HERE

**Web Interface:** http://127.0.0.1:5000

**Start Server:** `python3 server.py`

---

## 📊 What You Have

- **51 Main Recipes** - Your primary collection (Epicurious, NYT, Fergi, etc.)
- **85 Janet's Recipes** - Janet Mason cookbook (12 titled, 73 need titles)
- **136 Total Recipes** - All properly organized

---

## 🎯 Filter Buttons

| Button | Shows | Count |
|--------|-------|-------|
| **All Recipes** | Everything | 136 |
| **Main Recipes (51)** | Non-Janet recipes | 51 |
| **Janet's Recipes (85)** | Janet Mason only | 85 |
| **Needs Review (73)** | Recipes needing titles | 73 |
| **Statistics** | Database stats | - |

---

## 🎨 Visual Indicators

- **Orange Border + ⚠ Badge** = Needs title (click to edit!)
- **Purple Badge** = Janet's recipe
- **★ Gold Star** = Favorite
- **⭐⭐⭐** = Rating

---

## ✏️ Edit Recipe Workflow

1. Click recipe card
2. Click "Edit Recipe" button
3. Update title (remove "NEEDS TITLE")
4. Add ingredients/instructions if you want
5. Click "Save Changes"
6. Done!

---

## 📝 Janet Recipes - Already Titled (12)

1. Baking Powder Biscuits
2. Mango and Roasted Corn Salsa / Walking Fondue
3. Spinach Artichoke Dip
4. Fresh Tomato Bruschetta
5. Chinese Spring Rolls
6. Cowboy Caviar / Chicken Wings
7. Pork Beef Loaf / Spinach Filled Mushrooms
8. Josephinas Bread / Cheddar Pennies
9. Bourbon-Glazed Shrimp / Lamb on Skewers
10. Party Mix
11. Imperial Rolls
12. Mojito

**73 more** waiting for you to name them!

---

## 💡 Pro Tips

### Quick Title Update
1. Click "Needs Review (73)"
2. Click first orange-bordered recipe
3. Look at image in recipe detail
4. Click "Edit Recipe"
5. Replace title with what you see
6. Save & repeat

### Don't Overthink It
- Just get the titles in place
- You can refine everything later
- Use what you see in the cookbook image

### If You Can't Read the Image
- Make up a descriptive name
- Or use "Janet's [Type] Recipe #X"
- You can always change it later

---

## 🔧 Common Tasks

### Search for Recipe
- Use search box in nav bar
- Searches titles, ingredients, instructions

### Add to Favorites
- Open recipe → "Add to Favorites" button

### Rate Recipe
- Open recipe → Edit → Set rating (1-5)

### Delete Recipe
- Open recipe → "Delete Recipe" button
- ⚠️ Permanent! Be careful

---

## 📁 Important Files

- `recipes.db` - Your database (BACK THIS UP!)
- `index.html` - Web interface
- `UPDATED_WELCOME.md` - Full guide
- `Janet Mason/IMG_XXXX.JPG` - Original images

---

## 🆘 Troubleshooting

**Web interface won't load?**
- Start server: `python3 server.py`
- Check: http://127.0.0.1:5000

**Can't edit recipe?**
- Refresh the page
- Check browser console (F12) for errors

**Recipe images not showing?**
- Images are in `Janet Mason/` folder
- Check file path is correct

---

## 💾 Backup

```bash
cp recipes.db recipes_backup_$(date +%Y%m%d).db
```

---

## 📖 Documentation

| File | Purpose |
|------|---------|
| UPDATED_WELCOME.md | Comprehensive guide ← **Start here!** |
| QUICK_REFERENCE.md | This card (quick ref) |
| QUICKSTART.md | Original quick start |
| README.md | Full technical docs |
| PROJECT_SUMMARY.md | What was built |

---

## ✅ Your To-Do List

### Right Now
- [ ] Open http://127.0.0.1:5000
- [ ] Click "Needs Review (73)"
- [ ] Update first recipe title
- [ ] Pat yourself on the back!

### This Week
- [ ] Update all 73 Janet recipe titles
- [ ] Mark some favorites
- [ ] Rate recipes you've tried

### Ongoing
- [ ] Add notes as you cook
- [ ] Update ingredients/instructions
- [ ] Keep database backed up

---

**Everything is ready to go!**

**Just open:** http://127.0.0.1:5000

**Happy cooking!** 🍳
