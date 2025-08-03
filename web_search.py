from ddgs import DDGS

results = DDGS().text("LA Dodgers next game schedule", max_results=1)
print(results)