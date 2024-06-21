import submitHubspotForm from "@site/src/utils/submitHubspotForm";
import React, { useState } from "react";

const Newsletter = () => {
  const [formSubmitted, setFormSubmitted] = useState("initial");

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setFormSubmitted("loading");

    const formData = new FormData(e.target as HTMLFormElement);
    const email = formData.get("email") as string;

    try {
      await submitHubspotForm("3fe97f7a-b2ee-430b-b1c1-acf765bc7587", {
        email,
      });
      setFormSubmitted("success");
    } catch (error) {
      alert("An error occurred. Please try again.");
      setFormSubmitted("initial");
    }
  };

  return (
    <div className="container">
      {formSubmitted !== "success" ? (
        <>
          <p>Keep up to date with Dragonfly</p>
          <form onSubmit={handleSubmit}>
            <input
              type="email"
              name="email"
              required
              placeholder="Enter your email"
            />
            <button
              type="submit"
              className="btn-primary"
              disabled={formSubmitted === "loading"}
            >
              Submit
            </button>
          </form>
        </>
      ) : (
        <p>Thank you for subscribing to our newsletter!</p>
      )}
    </div>
  );
};

export default Newsletter;
