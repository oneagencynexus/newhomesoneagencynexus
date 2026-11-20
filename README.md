# One Agency Nexus — House & Land landing page

The site is built automatically from `projects.json` and the `images/` folder.
Every change to either file is published by GitHub within 1–2 minutes. No manual build is needed.

## Add a package
1. Upload three pictures to `images/` (Add file → Upload files):
   - facade (render without any developer or street name), e.g. `w_suburb.jpg`
   - interior, `i_<id>.jpg`
   - floor plan, `p_<id>.jpg`
2. Open `projects.json`, copy an existing block, paste it at the end of the list and change the values.
   - `id`: short lowercase name, no spaces (e.g. `newsuburb`)
   - `reg_`: `south`, `west`, `north` or `coast`
   - `ll`: [latitude, longitude]
   - `rent`: [weekly min, weekly max], add `"est": true` if it is our estimate
   - `dev`: one letter code (internal key)
   - `img`, `interior`, `plan`: the file names you uploaded
3. Commit. The site updates by itself. If something is wrong, the **Actions** tab shows what to fix.

## Remove or hide a package
Change `"status": "active"` to `"status": "sold"` (the block stays in the file but disappears from the page), or delete the block.

## Change a price
Edit `price` (and `lp` / `bp` if used) in `projects.json`.

## Rules for every package
- No developer, builder, estate name, lot number or street name on the page or in the pictures.
- Rent figures that are our own estimates must have `"est": true`.
- Check the price and availability before publishing.

## Local preview (optional)
`python3 build.py` then open `dist/index.html`.
