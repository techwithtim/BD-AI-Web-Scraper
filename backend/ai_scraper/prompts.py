JAVASCRIPT_PLAYWRIGHT = """const pw = require('playwright');

const SBR_CDP = '<enter yours>';

async function main() {
    console.log('Connecting to Scraping Browser...');
    const browser = await pw.chromium.connectOverCDP(SBR_CDP);
    try {
        const page = await browser.newPage();
        console.log('Connected! Navigating to https://example.com...');
        await page.goto('https://example.com');
        // CAPTCHA handling: To check the status of Scraping Browser's automatic CAPTCHA solver on the target page
        // const client = await page.context().newCDPSession(page);
        // console.log('Waiting captcha to solve...');
        // const { status } = await client.send('Captcha.waitForSolve', {
        //     detectTimeout: 10000,
        // });
        //console.log('Captcha solve status:', status);
        console.log('Navigated! Scraping page content...');
        const html = await page.content();
        console.log(html);
    } finally {
        await browser.close();
    }
}

main().catch(err => {
    console.error(err.stack || err);
    process.exit(1);
});"""

JAVASCRIPT_PUPPETEER = """const puppeteer = require('puppeteer-core');

const SBR_WS_ENDPOINT = '<enter yours>;

async function main() {
    console.log('Connecting to Scraping Browser...');
    const browser = await puppeteer.connect({
        browserWSEndpoint: SBR_WS_ENDPOINT,
    });
    try {
        const page = await browser.newPage();
        console.log('Connected! Navigating to https://example.com...');
        await page.goto('https://example.com');
        // CAPTCHA handling: If you're expecting a CAPTCHA on the target page, use the following code snippet to check the status of Scraping Browser's automatic CAPTCHA solver
        // const client = await page.createCDPSession();
        // console.log('Waiting captcha to solve...');
        // const { status } = await client.send('Captcha.waitForSolve', {
        //     detectTimeout: 10000,
        // });
        // console.log('Captcha solve status:', status);
        console.log('Navigated! Scraping page content...');
        const html = await page.content();
        console.log(html)
    } finally {
        await browser.close();
    }
}

main().catch(err => {
    console.error(err.stack || err);
    process.exit(1);
});"""

JAVASCRIPT_SELENIUM = """const { Builder, Browser } = require('selenium-webdriver');

const SBR_WEBDRIVER = '<enter yours>';

async function main() {
    console.log('Connecting to Scraping Browser...');
    const driver = await new Builder()
        .forBrowser(Browser.CHROME)
        .usingServer(SBR_WEBDRIVER)
        .build();
    try {
        console.log('Connected! Navigating to https://example.com...');
        await driver.get('https://example.com');
        // CAPTCHA handling: If you're expecting a CAPTCHA on the target page, use the following code snippet to check the status of Scraping Browser's automatic CAPTCHA solver
        // console.log('Waiting captcha to solve...');
        // const { status } = await driver.sendAndGetDevToolsCommand(
        //     'Captcha.waitForSolve', {
        //     detectTimeout: 10000,
        // });
        // console.log('Captcha solve status:', status);
        console.log('Navigated! Scraping page content...');
        const html = await driver.getPageSource();
        console.log(html);
    } finally {
        driver.quit();
    }
}

main().catch(err => {
    console.error(err.stack || err);
    process.exit(1);
});"""

PYTHON_SELENIUM = """from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection

SBR_WEBDRIVER = '<enter yours>'


def main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating to https://example.com...')
        driver.get('https://example.com')
        # CAPTCHA handling: If you're expecting a CAPTCHA on the target page, use the following code snippet to check the status of Scraping Browser's automatic CAPTCHA solver
        # print('Waiting captcha to solve...')
        # solve_res = driver.execute('executeCdpCommand', {
        #     'cmd': 'Captcha.waitForSolve',
        #     'params': {'detectTimeout': 10000},
        # })
        # print('Captcha solve status:', solve_res['value']['status'])
        print('Navigated! Scraping page content...')
        html = driver.page_source
        print(html)


if __name__ == '__main__':
    main()"""

PYTHON_PLAYWRIGHT = """import asyncio
from playwright.async_api import async_playwright

SBR_WS_CDP = '<enter yours>'


async def run(pw):
    print('Connecting to Scraping Browser...')
    browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    try:
        page = await browser.new_page()
        print('Connected! Navigating to https://example.com...')
        await page.goto('https://example.com')
        # CAPTCHA handling: If you're expecting a CAPTCHA on the target page, use the following code snippet to check the status of Scraping Browser's automatic CAPTCHA solver
        # client = await page.context.new_cdp_session(page)
        # print('Waiting captcha to solve...')
        # solve_res = await client.send('Captcha.waitForSolve', {
        #     'detectTimeout': 10000,
        # })
        # print('Captcha solve status:', solve_res['status'])
        print('Navigated! Scraping page content...')
        html = await page.content()
        print(html)
    finally:
        await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == '__main__':
    asyncio.run(main())"""
    

CSHARP_SELENIUM = """using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Remote;

var SBR_WEBDRIVER = "<enter yours>";

Console.WriteLine("Connecting to Scraping Browser...");
var options = new ChromeOptions();
using var driver = new RemoteWebDriver(new Uri(SBR_WEBDRIVER), options);
Console.WriteLine("Connected! Navigating to https://example.com...");
driver.Navigate().GoToUrl("https://example.com");
// CAPTCHA handling: If you're expecting a CAPTCHA on the target page, use the following code snippet to check the status of Scraping Browser's automatic CAPTCHA solver
// Console.WriteLine("Waiting captcha to solve...");
// var solve_res = driver.ExecuteCustomDriverCommand(ChromeDriver.ExecuteCdp,
// new (){
//     {"cmd", "Captcha.waitForSolve"},
//     {"params", new Dictionary<string, object>(){
//         {"detectTimeout", 10000},
//     }},
// }) as Dictionary<string, object>;
// Console.WriteLine("Captcha solve status: " + solve_res["status"]);
Console.WriteLine("Navigated! Scraping page content...");
var html = driver.PageSource;
Console.WriteLine(html);"""

CSHARP_PLAYWRIGHT = """using Microsoft.Playwright;

var SBR_CDP = "<enter yours>";

Console.WriteLine("Connecting to Scraping Browser...");
using var pw = await Playwright.CreateAsync();
await using var browser = await pw.Chromium.ConnectOverCDPAsync(SBR_CDP);
var page = await browser.NewPageAsync();
Console.WriteLine("Connected! Navigating to https://example.com...");
await page.GotoAsync("https://example.com");
// CAPTCHA handling: If you're expecting a CAPTCHA on the target page, use the following code snippet to check the status of Scraping Browser's automatic CAPTCHA solver
// var client = await page.Context.NewCDPSessionAsync(page);
// Console.WriteLine("Waiting captcha to solve...");
// var solve_res = await client.SendAsync("Captcha.waitForSolve", new ()
// {
//     {"detectTimeout", 10000},
// });
// var status = solve_res.Value
//     .GetProperty("status")
//     .GetString();
// Console.WriteLine("Captcha solve status: " + status);
Console.WriteLine("Navigated! Scraping page content...");
var html = await page.ContentAsync();
Console.WriteLine(html);"""

CSHARP_PUPPETEER = """using PuppeteerSharp;
using System.Net.WebSockets;
using System.Text;

var SBR_WS_ENDPOINT = "<enter yours>";

var Connect = (string ws) => Puppeteer.ConnectAsync(new ()
{
    BrowserWSEndpoint = ws,
    WebSocketFactory = async (url, options, cToken) => {
        var socket = new ClientWebSocket();
        var authBytes = Encoding.UTF8.GetBytes(new Uri(ws).UserInfo);
        var authHeader = "Basic " + Convert.ToBase64String(authBytes);
        socket.Options.SetRequestHeader("Authorization", authHeader);
        socket.Options.KeepAliveInterval = TimeSpan.Zero;
        await socket.ConnectAsync(url, cToken);
        return socket;
    },
});

Console.WriteLine("Connecting to Scraping Browser...");
using var browser = await Connect(SBR_WS_ENDPOINT);
var page = await browser.NewPageAsync();
Console.WriteLine("Connected! Navigating to https://example.com...");
await page.GoToAsync("https://example.com");
Console.WriteLine("Navigated! Scraping page content...");
var html = await page.GetContentAsync();
Console.WriteLine(html);"""

BD_EXAMPLES = {
    "javascript": {
        "selenium": JAVASCRIPT_SELENIUM,
        "playwright": JAVASCRIPT_PLAYWRIGHT,
        "puppeteer": JAVASCRIPT_PUPPETEER
    },
    "python": {
        "selenium": PYTHON_SELENIUM,
        "playwright": PYTHON_PLAYWRIGHT,
    },
    "c#": {
        "selenium": CSHARP_SELENIUM,
        "playwright": CSHARP_PLAYWRIGHT,
        "puppeteer": CSHARP_PUPPETEER
    }
}

def get_prompt(language, library, with_bd=False):
    additional_data = ""
    if with_bd:
        code = BD_EXAMPLES.get(language, {}).get(library, None)
        if not code:
            raise Exception("Invalid language or library combination.")
        additional_data = f"""When generating this code, use the code snippet below as a starting point so that it uses a brightdata scraping browser: 
                {code}
            """
    
    return f"""
            You are an AI assistant specialized in generating web scraping code based on provided DOM sections and user specifications. Your task is to analyze the given HTML structure and create efficient, accurate scraping code using the specified library (Selenium, Playwright, or Puppeteer) in either JavaScript or Python.

            Input:

            A section of HTML DOM (which may be large and provided in chunks)
            User's data extraction requirements
            Preferred scraping library (Selenium, Playwright, or Puppeteer)
            Preferred programming language (JavaScript, Python or C#)

            Context:
            The DOM content provided represents only the most relevant sections of the webpage, not the entire site. These sections have been extracted based on their relevance to the scraping task. Your goal is to focus on these specific sections to generate the most efficient scraping code.

            Output:
            Generate web scraping code that:

            Navigates to the correct elements within the provided DOM structure
            Extracts the specified data accurately
            Handles potential errors and edge cases
            Follows best practices for the chosen library and language
            {additional_data}

            Output Format:
            Your response must strictly adhere to the following format:
            [SETUP_INSTRUCTIONS]
            Any necessary setup instructions (e.g., library installation)
            [/SETUP_INSTRUCTIONS]

            [SCRAPING_CODE]
            # Generated scraping code here
            # Include comments explaining key steps
            [/SCRAPING_CODE]

            Guidelines:

            1. Process DOM chunks as they are received. Do not wait for all chunks before beginning analysis.
            2. Focus on the provided DOM sections, understanding that they represent the most relevant parts of the webpage for the scraping task.
            3. Analyze the DOM structure carefully to identify the most efficient selectors (e.g., IDs, classes, XPaths).
            4. Prioritize robust and maintainable code that can handle variations in the DOM structure.
            5. Include comments explaining key steps in the scraping process.
            6. If the DOM structure is unclear or ambiguous, state your assumptions and proceed with the best possible approach.
            7. Suggest improvements or alternative approaches if you identify more efficient methods.
            8. Ensure all code is contained within the [SCRAPING_CODE] tags.
            9. Provide a clear, concise summary within the [SCRAPING_SUMMARY] tags, including any assumptions made about the DOM structure.
            10. Include any necessary setup instructions within the [SETUP_INSTRUCTIONS] tags.

            Remember:
            - The provided DOM sections are pre-selected for relevance, so focus on these specific parts.
            - Your code should be adaptable to potential variations in the full website structure.
            - Emphasize error handling and robustness, as the full webpage may contain elements not present in the provided sections.
            - Insert the correct URL that comes from the user prompt in the finished code

            Example User Prompt:
            "Extract all product names and prices from the provided e-commerce page"""    