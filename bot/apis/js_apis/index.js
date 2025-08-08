import { Hono } from 'hono';
import mathRouter from './math/mathjs.js';
import { logger } from './utils/logger.js';

const app = new Hono();

app.use('*', logger);

// healthcheck
app.get('/ping', (c) => c.text('pong'));

// routes
app.route('/mathjs', mathRouter);

export default app;
