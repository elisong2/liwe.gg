import Navbar from "@/components/Navbar";
export default function About() {
  return (
    <>
      <Navbar></Navbar>
      <br />
      <h1>Thanks for stopping by!</h1>

      <p>
        This site is intended to be a fun ongoing testbed for interesting stats
        recorded by the Riot API. Some years ago, Riot used to do a season end
        review in the League client that showed various personal stats
        throughout the season. I am aiming to bring that back.
      </p>
    </>
  );
}
