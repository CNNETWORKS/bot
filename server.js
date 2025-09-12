// server.js
import express from "express";
import puppeteer from "puppeteer";

const app = express();

app.get("/numbers/:mobile", async (req, res) => {
  const { mobile } = req.params;

  try {
    const browser = await puppeteer.launch({
      headless: true,
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-accelerated-2d-canvas",
        "--no-first-run",
        "--no-zygote",
        "--single-process",
        "--disable-gpu"
      ],
    });

    const page = await browser.newPage();

    const url = `https://numlooking.rf.gd/index.php?key=376f2223a3afb769&num=${mobile}`;
    await page.goto(url, { waitUntil: "networkidle2" });

    // Wait for body text
    const bodyText = await page.evaluate(() => document.body.innerText);

    await browser.close();

    // Try parse JSON (agar site valid JSON deti hai to)
    try {
      const jsonData = JSON.parse(bodyText);
      res.json(jsonData); // JSON as-is return
    } catch (e) {
      res.send(bodyText); // fallback agar valid JSON na ho
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000, () => console.log("✅ Server running on http://localhost:3000"));
