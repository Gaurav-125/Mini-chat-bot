import express, { response } from "express"
import bodyParser from "body-parser"
import axios  from "axios"
import * as cheerio from "cheerio"

const app=express();
const port=3000;

app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));



app.get("/",(req,res) => {
    res.render("index.ejs",{response: []});
});

app.post("/submit",async(req,res)=>{
    // res.send("Hello");
    const userquery=req.body.query?.toLowerCase();
    try {
      console.log("Fetching URL...");
    // Fetch the static HTML page
    const { data } = await axios.get(process.env.FACULTY_URL,{
  headers: {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
  }
});
    console.log("URL Fectched Successfully");
    console.log("Data length:",data.length);

    // Load HTML into Cheerio
    const $ = cheerio.load(data);

    
    const facultyNames = []
     $("div.wmts_text_container").each((i, el) => {
      // console.log(`processing container ${i}`);
      const name=$(el).find("h2.wmts_name").text().trim();
      const email=$(el).find("div.wmts_attribute span[data-wph-type='value'] span a[href^='mailto:']").attr("href");
//     const emailTag = $(el).find("div.wmts_attribute span[data-wph-type='value'] a[href^='mailto:']");
//   const email = emailTag.length ? emailTag.text().trim() : "No email listed";
  
      const linkedin=$(el).find("div.wmts_links a[href*='linkedin.com']").attr("href");
      const facebook=$(el).find("div.wmts_links a[href*='facebook.com']").attr("href");
      const X_acc=$(el).find("div.wmts_links a[href*='twitter.com']").attr("href");
      const instagram=$(el).find("div.wmts_links a[href*='instagram.com']").attr("href");
      const site=$(el).find("div.wmts_links a[href*='sites.google.com']").attr("href");
      // console.log($(el).html());

      facultyNames.push({
        name,
        email: email ? email.replace("mailto:", "") : "No email listed",
        linkedin: linkedin || "No linkedin",
        facebook: facebook || "No facebook",
        X_acc: X_acc || "No X-account",
        instagram: instagram || "No Instagram",
        site: site || "No site"
      });
    });

    let filteredData=facultyNames;
    if(userquery){
        filteredData=facultyNames.filter(faculty => 
            faculty.name.toLowerCase().includes(userquery)
        );
    }
    // if no match found
    if(filteredData.length===0){
        res.render("index.ejs",{response: []})
    }else{
        res.render("index.ejs",{response: filteredData})
    }

    // Render back into EJS
    // res.render("index.ejs", { response: facultyNames});
  } catch (err) {
    console.log("URL not fetched");
    res.render("index.ejs", { response: [] });
  }

    // res.render("index.ejs",{response: `You asked: ${userquery}`});
});

app.listen(port,"0.0.0.0",() => {
    console.log(`Server running on port ${port}`);
});
