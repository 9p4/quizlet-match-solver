use std::collections::HashMap;
use std::io;
use std::io::prelude::*;
use thirtyfour::prelude::*;
use tokio;

fn pause(msg: &str) {
    let mut stdin = io::stdin();
    let mut stdout = io::stdout();

    // We want the cursor to stay at the end of the line, so we print without a newline and flush manually.
    write!(stdout, "{}", msg).unwrap();
    stdout.flush().unwrap();

    // Read a single byte and discard
    let _ = stdin.read(&mut [0u8]).unwrap();
}

async fn scan(driver: &WebDriver) -> WebDriverResult<HashMap<String, String>> {
    let terms = driver.find_elements(By::Css("[aria-label='Term']")).await?;
    let mut term_data = HashMap::new();
    for term in terms {
        let values = term.find_elements(By::ClassName("TermText")).await?;
        term_data.insert(values[0].text().await?, values[1].text().await?);
    }
    Ok(term_data)
}

async fn play(driver: &WebDriver, term_data: &HashMap<String, String>) -> WebDriverResult<()> {
    driver
        .find_element(By::Css("[aria-label='Start game']"))
        .await?
        .click()
        .await?;
    println!("Starting!");
    println!("Looking for cards...");
    let cards = driver
        .find_elements(By::ClassName("MatchModeQuestionGridTile"))
        .await?;
    let mut card_data: HashMap<String, WebElement> = HashMap::new();
    for card in &cards {
        println!("Adding card...");
        card_data.insert(
            card.find_element(By::ClassName("MatchModeQuestionGridTile-text"))
                .await?
                .get_attribute("aria-label")
                .await?
                .unwrap(),
            card.clone(),
        );
    }
    for (card_key, _) in &card_data {
        println!("Card key {}", card_key);
        if term_data.contains_key(card_key) {
            card_data[card_key].click().await?;
            card_data[&term_data[card_key]].click().await?;
        }
    }
    Ok(())
}

#[tokio::main]
async fn main() -> WebDriverResult<()> {
    let caps = DesiredCapabilities::firefox();
    let driver = WebDriver::new("http://localhost:4444", &caps).await?;
    driver.get("https://quizlet.com").await?;
    pause("Press enter when you've logged in and opened the Quizlet set. You may need to scroll down to load all the terms.");
    let term_data = scan(&driver).await?;
    println!("Found {} terms", term_data.len());
    pause("Press enter when the match game has loaded (do not start it yet! This program will do that for you)");
    play(&driver, &term_data).await?;
    pause("Completed!");
    Ok(())
}
