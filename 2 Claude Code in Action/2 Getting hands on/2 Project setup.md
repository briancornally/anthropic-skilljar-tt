## Project setup

- https://anthropic.skilljar.com/claude-code-in-action/301615

Working with Claude Code is more interesting if you have a project to work with.

I've put together a small project to explore with Claude Code. It is the same UI generation app shown in a previous video. **Note:** you don't have to run this project. You can always follow along with the remainder of the course with your own code base if you wish!

**Setup**

This project requires a small amount of setup:

1. Ensure you have Node JS installed locally. [Link to installation directions](https://nodejs.org/en/download).
2. Download the zip file called `uigen.zip` attached to this lecture and extract it
3. In the project directory, run `npm run setup` to install dependencies and set up a local SQLite database
4. **Optional:** this project uses Claude through the Anthropic API to generate UI components. If you want to fully test out the app, you will need to provide an API key to access the Anthropic API. _This is optional. If no API key is provided, the app will still generate some static fake code._ Here's how you can set the api key:
   1. Get an Anthropic API key at https://console.anthropic.com/
   2. Place your API key in the `.env` file.
5. Start the project by running `npm run dev`

#### Downloads

https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic/assets/1769622681/uigen.zip?response-content-disposition=attachment&Expires=1776511067&Signature=BFw3VRYTbMU9EzvauXpvil-OJ56KZxFcP~VEmW3PRhbIoqVcJOb5K2RmLfhl1Pg0Ka1W3B8YSIxXRrcCFF0KCJFcx0dmPAaXaRXJz72zcUuUt2A0NqUU9enKQSlUArcLUua3s7z~MdR998QjITkWtsiftCX7mzQVSmyFkYcajo9lFCVoRw~vbTYPvlX7x-rmzd7AVYQvHz-UVN7YBgRrojR9182EOJMmK64H-gpKhFU8EBxms7E6jvzfkMNcyI1HOelNuUWn4Ds-ea4w-eJprgGoKz~XqADmJqbOumXdbIjP6shIVZAwK7gpiHWp~OoXW2IhXdSDoIbgy0hDklKx6A__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ
