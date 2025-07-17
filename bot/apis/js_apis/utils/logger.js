import chalk from "chalk";

export const logger = async (c, next) => {
  const start = process.hrtime.bigint();
  await next();
  const end = process.hrtime.bigint();
  const durationNs = end - start;

  let formatted;
  if (durationNs < 1_000n) {
    formatted = `${durationNs}ns`;
  } else if (durationNs < 1_000_000n) {
    formatted = `${(Number(durationNs) / 1_000).toFixed(2)}μs`;
  } else {
    formatted = `${(Number(durationNs) / 1_000_000).toFixed(2)}ms`;
  }

  const {method, path} = c.req;
  const {status} = c.res;

  console.log(
    `${chalk.gray(new Date().toISOString())} ` +
    `${chalk.green(method)} ${chalk.blue(path)} ` +
    `${chalk.yellow(status)} ${chalk.magenta(formatted)}`
  );
};
