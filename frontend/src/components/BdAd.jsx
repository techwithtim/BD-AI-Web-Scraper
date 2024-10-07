import "../css/BdAd.css"
import React from 'react';
import bdLogo from "../assets/bd-logo.png"

const ScaleUpScraping = ({library}) => {
  return (
    <div className="scale-up-container">
      <h1>Ready to Scale Up Your Web Scraping?</h1>
      <p className="subtitle">
        You've built your {library} web scraper, now it's time to scale up by
        running it using Bright Data to ensure reliability, scale, and avoid blocks!
      </p>
      
      <div className="steps-container">
        <div className="step">
          <div className="step-number">1</div>
          <h2>Sign Up for Free</h2>
          <p><a>Get started with $25 in free credits</a> on Bright Data.</p>
        </div>
        
        <div className="step">
          <div className="step-number">2</div>
          <h2>Use Scraping Browser</h2>
          <p>For automated scraping. <a>Learn more here.</a></p>
        </div>
        
        <div className="step">
          <div className="step-number">3</div>
          <h2>Run</h2>
          <p>Integrate Bright Data proxies, run your script and scale!</p>
        </div>
      </div>
      
      <p className="powered-by">
        Power up your data collection with <img className="bright-data" src={bdLogo}></img>
      </p>
    </div>
  );
};

export default ScaleUpScraping;