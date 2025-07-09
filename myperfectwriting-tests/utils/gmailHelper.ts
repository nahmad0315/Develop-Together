// import { google } from "googleapis";
// import path from "path";
// import fs from "fs";
// import { authenticate } from "@google-cloud/local-auth";
// import { OAuth2Client } from "google-auth-library";

// const SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"];
// const TOKEN_PATH = path.join(process.cwd(), "token.json");
// const CREDENTIALS_PATH = path.join(process.cwd(), "credentials.json");

// async function loadSavedCredentialsIfExist(): Promise<OAuth2Client | null> {
//   try {
//     const content = await fs.promises.readFile(TOKEN_PATH, "utf-8");
//     const credentials = JSON.parse(content);
//     const client = google.auth.fromJSON(credentials) as OAuth2Client;

//     if (!client.credentials.refresh_token) return null;

//     return client;
//   } catch (err) {
//     return null;
//   }
// }

// async function saveCredentials(client: OAuth2Client) {
//   const credentials = await fs.promises.readFile(CREDENTIALS_PATH, "utf-8");
//   const keys = JSON.parse(credentials);
//   const key = keys.installed || keys.web;
//   const payload = JSON.stringify({
//     type: "authorized_user",
//     client_id: key.client_id,
//     client_secret: key.client_secret,
//     refresh_token: client.credentials.refresh_token,
//   });
//   await fs.promises.writeFile(TOKEN_PATH, payload);
// }

// export async function authorizeGmail(): Promise<OAuth2Client> {
//   let client = await loadSavedCredentialsIfExist();

//   if (!client) {
//     client = (await authenticate({
//       scopes: SCOPES,
//       keyfilePath: CREDENTIALS_PATH,
//     })) as unknown as OAuth2Client;

//     if (!client.credentials.refresh_token) {
//       throw new Error("Authorization failed: No refresh token returned.");
//     }

//     await saveCredentials(client);
//   }

//   return client;
// }

// function delay(ms: number) {
//   return new Promise((resolve) => setTimeout(resolve, ms));
// }

// export async function getVerificationLink(email: string): Promise<string> {
//   const auth = await authorizeGmail();
//   const gmail = google.gmail({ version: "v1", auth });

//   const maxRetries = 12; // 12 * 5s = 60s total wait
//   const retryDelay = 5000;
//   let messageId: string | null | undefined; // ✅ FIXED LINE

//   for (let attempt = 1; attempt <= maxRetries; attempt++) {
//     const res = await gmail.users.messages.list({
//       userId: "me",
//       q: 'subject:"One Click to Activate Your Account" newer_than:1d',
//       maxResults: 5,
//     });

//     messageId = res.data.messages?.[0]?.id;

//     if (messageId) break;

//     console.log(
//       `Attempt ${attempt}: Email not found. Retrying in ${
//         retryDelay / 1000
//       }s...`
//     );
//     await delay(retryDelay);
//   }

//   if (!messageId) throw new Error("No verification email found after waiting.");

//   const msg = await gmail.users.messages.get({
//     userId: "me",
//     id: messageId,
//     format: "full",
//   });

//   const parts = msg.data.payload?.parts;
//   let bodyData = "";

//   if (parts) {
//     const htmlPart = parts.find((p) => p.mimeType === "text/html");
//     bodyData = htmlPart?.body?.data || "";
//   } else {
//     bodyData = msg.data.payload?.body?.data || "";
//   }

//   const decoded = Buffer.from(
//     bodyData.replace(/-/g, "+").replace(/_/g, "/"),
//     "base64"
//   ).toString("utf-8");

//   const linkMatch = decoded.match(
//     /https:\/\/portal\.myperfectwriting\.co\.uk\/verify-email[^">]*/
//   );

//   if (!linkMatch) throw new Error("Verification link not found.");
//   return linkMatch[0];
// }

import { google } from "googleapis";
import path from "path";
import fs from "fs";
import { authenticate } from "@google-cloud/local-auth";
import { OAuth2Client } from "google-auth-library";

const SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"];
const TOKEN_PATH = path.join(process.cwd(), "token.json");
const CREDENTIALS_PATH = path.join(process.cwd(), "credentials.json");

async function loadSavedCredentialsIfExist(): Promise<OAuth2Client | null> {
  try {
    const content = await fs.promises.readFile(TOKEN_PATH, "utf-8");
    const credentials = JSON.parse(content);
    const client = google.auth.fromJSON(credentials) as OAuth2Client;

    if (!client.credentials.refresh_token) return null;

    return client;
  } catch (err) {
    return null;
  }
}

async function saveCredentials(client: OAuth2Client) {
  const credentials = await fs.promises.readFile(CREDENTIALS_PATH, "utf-8");
  const keys = JSON.parse(credentials);
  const key = keys.installed || keys.web;
  const payload = JSON.stringify({
    type: "authorized_user",
    client_id: key.client_id,
    client_secret: key.client_secret,
    refresh_token: client.credentials.refresh_token,
  });
  await fs.promises.writeFile(TOKEN_PATH, payload);
}

export async function authorizeGmail(): Promise<OAuth2Client> {
  let client = await loadSavedCredentialsIfExist();

  if (!client) {
    client = (await authenticate({
      scopes: SCOPES,
      keyfilePath: CREDENTIALS_PATH,
    })) as unknown as OAuth2Client;

    if (!client.credentials.refresh_token) {
      throw new Error("Authorization failed: No refresh token returned.");
    }

    await saveCredentials(client);
  }

  return client;
}

function delay(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function getVerificationLink(email: string): Promise<string> {
  const auth = await authorizeGmail();
  const gmail = google.gmail({ version: "v1", auth });

  const maxRetries = 12; // 12 * 5s = 60s total wait
  const retryDelay = 5000;
  let messageId: string | null | undefined;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    const res = await gmail.users.messages.list({
      userId: "me",
      q: 'subject:"One Click to Activate Your Account" is:unread',
      maxResults: 5,
    });

    const messages = res.data.messages;
    if (!messages || messages.length === 0) {
      console.log(`Attempt ${attempt}: No emails found.`);
    } else {
      // Sort by internalDate DESC (latest first)
      const latest = messages[0];
      messageId = latest.id;
    }

    if (messageId) break;

    console.log(
      `Attempt ${attempt}: Email not found. Retrying in ${
        retryDelay / 1000
      }s...`
    );
    await delay(retryDelay);
  }

  if (!messageId) throw new Error("No verification email found after waiting.");

  const msg = await gmail.users.messages.get({
    userId: "me",
    id: messageId,
    format: "full",
  });

  const parts = msg.data.payload?.parts;
  let bodyData = "";

  if (parts) {
    const htmlPart = parts.find((p) => p.mimeType === "text/html");
    bodyData = htmlPart?.body?.data || "";
  } else {
    bodyData = msg.data.payload?.body?.data || "";
  }

  const decoded = Buffer.from(
    bodyData.replace(/-/g, "+").replace(/_/g, "/"),
    "base64"
  ).toString("utf-8");

  // This regex looks for href attributes that contain the domain myperfectwriting.co.uk
  const hrefMatch = decoded.match(
    /href="([^"]+myperfectwriting\.co\.uk[^"]+)"/i
  );

  if (!hrefMatch || !hrefMatch[1]) {
    throw new Error("Verification link not found.");
  }

  return decodeURIComponent(hrefMatch[1]);
}
