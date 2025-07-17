import { Hono } from 'hono';
import { evaluate, format } from 'mathjs';

const router = new Hono();
const cache = new Map();

const TTL_MS = 7 * 24 * 60 * 60 * 1000;

router.post('/evaluate', async (c) => {
  try {
    const { expression, precision } = await c.req.json();

    if (typeof expression !== 'string') {
      return c.json({ error: "Expected a string 'expression'" }, 400);
    }

    const cacheKey = `${expression}|${precision ?? 'default'}`;
    const now = Date.now();


    if (cache.has(cacheKey)) {
      const { result, expiresAt } = cache.get(cacheKey);
      if (expiresAt > now) {
        return c.json({ result, cached: true });
      } else {
        cache.delete(cacheKey);
      }
    }

    const rawResult = evaluate(expression);
    const result =
      typeof rawResult === 'number' && typeof precision === 'number'
        ? format(rawResult, { precision })
        : rawResult;

    cache.set(cacheKey, { result, expiresAt: now + TTL_MS });

    return c.json({ result, cached: false });
  } catch (err) {
    return c.json({ error: err.toString() }, 400);
  }
});

export default router;
