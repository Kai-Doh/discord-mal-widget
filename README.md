# Discord MAL Widget

Automatically sync your MyAnimeList stats to your Discord Profile Widget every 6 hours using GitHub Actions.

## Getting Started

> [!IMPORTANT]
> **Discord Profile Widgets (Experimental)**
>
> Discord Profile Widgets are currently an experimental feature. Follow [Chloe Cinders' Blog Guide](https://chloecinders.com/blog/discord-widgets) to enable the required Discord experiments, create and publish your widget, apply the **Application Identity** (a separate one-time OAuth authorization step — easy to miss, and required before the API will accept any updates), and add the widget to your Discord profile before continuing.

### 1. Fork this Repository

Click the **Fork** button at the top-right of this repository.

### 2. Add Widget Fields

Using the widget config editor described in the guide above, add the following fields:

| Field | Type | Description |
| ------ | ---- | ----------- |
| `avatar` | Media | MyAnimeList avatar |
| `joindate` | String | MyAnimeList join date |
| `dayswatched` | String | Total days of anime watched |
| `watching` | Number | Anime currently watching |
| `completed` | Number | Anime completed |
| `plantowatch` | Number | Anime plan to watch |
| `dropped` | Number | Anime dropped |
| `onhold` | Number | Anime on hold |
| `totalanime` | Number | Total anime entries |

### 3. Get Discord Credentials

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and select your app.
2. Copy the **Application ID** from General Information. (`APP_ID`)
3. Copy your Bot token from the **Bot** tab (click **Reset Token**). (`BOT_TOKEN`)
4. Click your profile in Discord and click **Copy User ID**. (`USER_ID`) (Note: If this option does not appear, enable **Developer Mode** first in Discord Settings -> Developer).

### 4. Configure GitHub Secrets

1. Go to your forked repository's **Settings** tab.
2. In the left sidebar, click **Secrets and variables -> Actions**.
3. Under the **Secrets** tab, click **New repository secret**.
4. Add the following secrets:

| Secret Name | Description |
| :--- | :--- |
| `BOT_TOKEN` | The Discord Bot Token (from Step 3) |
| `MAL_USERNAME` | Your MyAnimeList username |
| `APP_ID` | The Application ID of your Discord App (from Step 3) |
| `USER_ID` | Your Discord User ID (from Step 3) |

### 5. Run the GitHub Action

1. Go to the **Actions** tab of your repository.
2. *(First time only)* If prompted, click **"I understand my workflows, go ahead and enable them"**.
3. In the left sidebar under **Workflows**, select **Update Discord MAL Widget**.
4. Click the **Run workflow** dropdown and click the green **Run workflow** button to trigger the sync manually.

Once confirmed working, it will run automatically every 6 hours via the schedule in [`update-widget.yml`](.github/workflows/update-widget.yml).

## How It Works

[`refresh_mal.py`](refresh_mal.py) fetches your public MyAnimeList profile page directly (`https://myanimelist.net/profile/{username}`) and parses the stats out of the HTML with BeautifulSoup, rather than going through the Jikan API. Jikan's own user-scraping endpoints have been unreliable, while MyAnimeList's profile page is directly reachable and contains everything the widget needs.

## Local Development

1. Clone and install dependencies:
   ```bash
   git clone https://github.com/Kai-Doh/discord-mal-widget.git
   cd discord-mal-widget
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the root directory:
   ```env
   BOT_TOKEN=your_discord_bot_token
   MAL_USERNAME=your_mal_username
   APP_ID=your_discord_application_id
   USER_ID=your_discord_user_id
   ```
3. Run the sync script:
   ```bash
   python refresh_mal.py
   ```

## Troubleshooting

- **403 Forbidden from the Discord API**: almost always means the one-time **Application Identity** authorization step from Chloe Cinders' guide hasn't been completed for this application, or the widget hasn't been added to your profile. This is separate from having a valid bot token.
- **Jikan/MyAnimeList request errors**: MyAnimeList occasionally throttles or blocks scrapers. A failed run will simply retry on the next scheduled run 6 hours later, or you can manually re-run the Action.

## Credits

- Special thanks to [Chloe Cinders](https://chloecinders.com/blog/discord-widgets) for documenting Discord Profile Widgets and making this project possible.

## License

This project has no license file yet — add one if you plan to share or open this repository publicly.
