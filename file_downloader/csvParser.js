const fs = require("fs");
const csv = require("csv-parser");
const Handlebars = require("handlebars");
const pdf = require("html-pdf");

// Read the CSV file and generate an array of data objects
function parseCSV(csvFilePath) {
  return new Promise((resolve, reject) => {
    const results = [];
    fs.createReadStream(csvFilePath)
      .pipe(csv())
      .on("data", (row) => {
        results.push(row);
      })
      .on("end", () => {
        resolve(results);
      })
      .on("error", (error) => {
        reject(error);
      });
  });
}

// Generate the HTML using the data and template
function generateHTML(data, template) {
  const compiledTemplate = Handlebars.compile(template);
  return compiledTemplate(data);
}

// // Convert HTML to PDF
// function convertHTMLToPDF(htmlContent, pdfFilePath) {
//   pdf.create(htmlContent).toFile(pdfFilePath, (err, res) => {
//     if (err) {
//       console.error(err);
//     } else {
//       console.log("PDF generated successfully!");
//     }
//   });
// }

// Path to CSV file
const csvFilePath = "data.csv";

// Path to HTML template file
const templateFilePath = "index.html";

// Path to output HTML file
const outputHtmlFilePath = "output/";

// Path to output PDF file
const outputPdfFilePath = "output/";

// Read the CSV file and generate an array of data objects
parseCSV(csvFilePath)
  .then((data) => {
    // Read the HTML template file
    fs.readFile(templateFilePath, "utf-8", (err, template) => {
      if (err) {
        console.error("An error occurred:", err);
        return;
      }

      // Loop through the data array to generate individual HTML files
      data.forEach((item) => {
        // Generate the HTML content using the template and individual data object
        const generatedHtml = generateHTML(item, template);
        console.log(item);

        // Write the individual HTML files to disk
        const individualHtmlFilePath = `output${item.Name}.html`;
        fs.writeFile(individualHtmlFilePath, generatedHtml, (err) => {
          if (err) {
            console.error("An error occurred:", err);
            return;
          }
          console.log(
            `Individual HTML file generated: ${individualHtmlFilePath}`
          );
        });

        // Convert individual HTML files to PDF
        // const individualPdfFilePath = `output_${item.Name}.pdf`;
        // convertHTMLToPDF(generatedHtml, individualPdfFilePath);
      });
    });
  })
  .catch((error) => {
    console.error("An error occurred:", error);
  });
