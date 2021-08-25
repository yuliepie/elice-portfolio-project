export default function parseDate(dateString) {
  const dates = dateString.split("-");
  return {
    year: dates[0],
    month: dates[1],
    day: dates[2],
  };
}
