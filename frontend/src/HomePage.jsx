import React from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";


function HomePage() {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate("/upload");
  };

  return (
    <div className="App">
      {/* Hero Section */}
      <section className="qualtrics-hero">
  <div className="hero-content">
      <h1>Enhance Your Product with Kano Analysis</h1>
      <p>Visualize what truly matters to your customers with minimal effort.</p>
      <button className="btn-primary" onClick={handleGetStarted}>Get Started</button>
  </div>

</section>




      {/* Why Choose Us Section */}
      <section className="why-choose-us">
        <h2>Why Choose Us</h2>
        <div className="reasons-container">
          <div className="reason-card">
            <h3>When there are limited resources</h3>
            <p>
              The simple method for carrying out Kano analysis uses an email
              questionnaire, meaning that you don’t need expert resources to do
              the research.
            </p>
          </div>
          <div className="reason-card">
            <h3>When you want to see what would impress your customers</h3>
            <p>
              When you’re looking to ‘think outside of the box’, you can use
              Kano analysis to discover what features customers would value.
            </p>
          </div>
          <div className="reason-card">
            <h3>When you want to enhance a current product</h3>
            <p>
              Kano analysis helps assess your feature options and provides clear
              insights to keep your product competitive.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default HomePage;