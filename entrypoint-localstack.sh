
set -e

aws --endpoint-url=http://localhost:4566 ses verify-email-identity --email-address smtpmail195@gmail.com
