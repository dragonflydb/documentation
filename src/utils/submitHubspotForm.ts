import getCookie from "./getCookie";

const HS_PORTAL_ID = "23661280";

const submitHubspotForm = async (
  formId: string,
  fields: Record<string, unknown>,
  consent?: string | boolean
) => {
  const hutk = getCookie("hubspotutk");

  const data = {
    submittedAt: Date.now(),
    fields: Object.entries(fields)
      .map(([name, value]) => ({ name, value }))
      .filter((field) => field.name),
    context: {
      hutk,
      pageUri: window.location.href,
      pageName: document.title,
    },
    legalConsentOptions: consent
      ? {
          consent: {
            consentToProcess: true,
            text: consent,
          },
        }
      : undefined,
  };

  const response = await fetch(
    `https://api.hsforms.com/submissions/v3/integration/submit/${HS_PORTAL_ID}/${formId}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }
  );
  const body = await response.json();

  if (body.status === "error") {
    throw new Error(body.errors.map((error: any) => error.message).join("\n"));
  }

  return body;
};

export default submitHubspotForm;
