# chmod +x analyze-logs.sh
# ./analyze-logs.sh > container_logs.txt

# grep -i "error\|exception\|failed" container_logs.txt

containers=(
    "influxdb"
    "air-quality-probe"
    "air-voc-probe"
    "api-data-probe"
    "air-co2-temp-hum-probe"
    "air-co-voc-no2-c2h5oh-probe"
)

echo "=== Collecting last 50 lines of logs for each container ==="
for container in "${containers[@]}"; do
    echo -e "\n\n=== $container logs ===\n"
    docker logs --tail 50 "$container" 2>&1
done

echo -e "\n=== Container resource usage ===\n"
docker stats --no-stream "${containers[@]}"