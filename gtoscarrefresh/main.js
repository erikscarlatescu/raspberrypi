const axios = require("axios").default;
const cheerio = require("cheerio");
const nodemailer = require("nodemailer");
const cron = require("node-cron");

const url =
  "https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in=202202&crn_in=";

const links = [
  ["32618", [0, 2]], // 4649 WL
  ["27177", [0, 2]], // 3790
];
const emails = [
  "pranav.putta22@gmail.com",
  "kartiknarang@gmail.com",
  "escarlatescu3@gatech.edu",
];

let last_open_seats = new Array(links.length).fill(-1);
let last_open_waitlist = new Array(links.length).fill(-1);

async function main() {
  console.log("seats: " + last_open_seats);
  console.log(last_open_waitlist);
  links.forEach(async (crn, i) => {
    link = url + crn[0];
    axios.get(link).then(async (res) => {
      const $ = cheerio.load(res.data);
      const table = $(`span:contains("Remaining")`).parentsUntil("tbody").eq(3);
      const num_open_seats = table.find("tr").eq(1).find("td").eq(2).text();
      const num_open_waitlist = table.find("tr").eq(2).find("td").eq(2).text();
      let transport = nodemailer.createTransport({
        host: "smtp.gmail.com",
        port: 587,
        secure: false,
        auth: {
          user: "odysseyapp.us@gmail.com",
          pass: "redwedding69",
        },
      });
      if (last_open_seats[i] <= 0 && num_open_seats > 0) {
        // send email
        await transport.sendMail({
          from: "odysseyapp.us@gmail.com",
          to: crn[1].map((i) => emails[i]),
          subject: "Seat Available in CRN: " + crn[0],
          text: "check oscar u bastard",
        });
        console.log("there are seats!");
      }
      if (last_open_waitlist[i] <= 0 && num_open_waitlist > 0) {
        await transport.sendMail({
          from: "odysseyapp.us@gmail.com",
          to: crn[1].map((i) => emails[i]),
          subject: "Waitlist Seat Available in CRN: " + crn[0],
          text: "check oscar u bastard",
        });
        console.log("there are waitlist spots!");
      }

      last_open_seats[i] = num_open_seats;
      last_open_waitlist[i] = num_open_waitlist;
    });
  });
}

cron.schedule("*/10 * * * * *", () => {
  try {
    main();
  } catch {
    console.log("an error ocurred");
  }
});
main();
