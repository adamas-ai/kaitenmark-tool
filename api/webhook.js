export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(200).send('OK');

  const GAS_URL = "YOUR_GAS_URL"; // ここをあなたのGASの /exec に置換

  try {
    const r = await fetch(GAS_URL, {
      method: 'POST',
      headers: { 'content-type': 'application/json; charset=utf-8' },
      body: JSON.stringify(req.body),
    });
    const text = await r.text();
    return res.status(200).send(text || 'OK');
  } catch (e) {
    return res.status(200).send('OK');
  }
}
