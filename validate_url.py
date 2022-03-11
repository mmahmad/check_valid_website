import requests
import argparse

# Initial connection timeout. Will increase by 0.2s on each subsequent attempt.
TIMEOUT_SECONDS = 0.2
# Number of times to attempt to connect, increasing timeout by 0.2s each time
TOTAL_ATTEMPTS = 5
# Input file containing URL, 1 on each line
INPUT_FILE = "sample.txt"
# Output file containing failed URLs
OUTPUT_FILE = "failed_urls.txt"


def check_url_exists(url, timeout):
    """
    Checks if a url exists by retrieving headers and check if the response status code is 200
    :param url: url to check
    :param allow_redirects=True
    :param timeout in seconds
    :return: True if the url exists, false otherwise.
    """
    return requests.head(url, allow_redirects=True, timeout=timeout).status_code == 200


def write_urls_to_file(failed_urls, output_file):
    """
    Write given failed URLs to a file, one URL on each line
    :param failed_urls: list of failed urls
    :param output_file: output file to write the failed URLs
    """
    with open(output_file, "x+") as of:
        for failed_url in failed_urls:
            of.write(failed_url)


def main(input_args):
    timeout_seconds = TIMEOUT_SECONDS

    # Received from the input command. If none provided, default values used
    input_file = input_args.input
    output_file = input_args.output
    total_attempts = input_args.attempts
    assert total_attempts > 0

    # Store URLs that time out. If
    urls_timed_out = []
    current_attempt = 1

    # Read URL line-by-line from file, and check if each URL is reachable. If not, add the URL to urls_timed_out list.
    with open(input_file, 'r') as f:
        for line in f:
            u = line.strip()
            try:
                print(f"(attempt {current_attempt}/{total_attempts}) checking url: {u} with timeout {timeout_seconds}")
                if check_url_exists(u, timeout_seconds):
                    print(f"{u} is valid")
            except:
                print(f"{u} was unreachable.")
                # urls_timed_out[u].append(timeout)
                urls_timed_out.append(u)

    current_attempt += 1  # should be 2

    # if attempts > 1, retry
    while current_attempt <= total_attempts and len(urls_timed_out) > 0:
        timeout_seconds += 0.2
        print(f"Setting timeout to {timeout_seconds}")
        for retry_url in urls_timed_out:
            try:
                print(
                    f"retrying url (attempt {current_attempt}/{total_attempts}): {retry_url} with timeout {timeout_seconds}s.")
                if check_url_exists(retry_url, timeout_seconds):
                    print(f"{retry_url} is valid")
                    # remove url from list
                    urls_timed_out[:] = [x for x in urls_timed_out if not retry_url]
                    # urls_timed_out.remove(retry_url)
            except:
                print(f"retryUrl {retry_url} is not valid with timeout {timeout_seconds}s.")
                # urls_timed_out[u].append(timeout)
                # urls_timed_out.append(retry_url)

        current_attempt += 1

    # write failed URLs to file
    write_urls_to_file(urls_timed_out, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input text file name (including.txt). Must be in the root directory.", default=INPUT_FILE)
    parser.add_argument("-o", "--output", help="Output file name (including .txt). Will be in the root directory.", default=OUTPUT_FILE)
    parser.add_argument("-a", "--attempts", help="Number of total attempts before giving up.", type=int, default=TOTAL_ATTEMPTS)
    args = parser.parse_args()

    if args.attempts < 1:
        raise Exception("attempts must be > 0")

    main(args)
