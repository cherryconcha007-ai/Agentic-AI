{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOL6uzjCwR7dVsmDdmj7pOW",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/cherryconcha007-ai/Agentic-AI/blob/main/streamlit_app.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 383
        },
        "id": "lh7XhL5pW2Vq",
        "outputId": "895480f2-bad7-4125-a9c0-4de8e723e7ee"
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "ModuleNotFoundError",
          "evalue": "No module named 'streamlit'",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipykernel_13969/1846383882.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mstreamlit\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mst\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      2\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mpandas\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mpd\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;31m# 1. Setup\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0mst\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mset_page_config\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mpage_title\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;34m\"AI Factory Analytics\"\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mlayout\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;34m\"wide\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'streamlit'",
            "",
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0;32m\nNOTE: If your import is failing due to a missing package, you can\nmanually install dependencies using either !pip or !apt.\n\nTo view examples of installing some common dependencies, click the\n\"Open Examples\" button below.\n\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n"
          ],
          "errorDetails": {
            "actions": [
              {
                "action": "open_url",
                "actionText": "Open Examples",
                "url": "/notebooks/snippets/importing_libraries.ipynb"
              }
            ]
          }
        }
      ],
      "source": [
        "import streamlit as st\n",
        "import pandas as pd\n",
        "\n",
        "# 1. Setup\n",
        "st.set_page_config(page_title=\"AI Factory Analytics\", layout=\"wide\")\n",
        "st.title(\"🏆 AI Factory Growth Equity Sandbox\")\n",
        "\n",
        "# 2. Initial Data\n",
        "data = [\n",
        "    {\"Company\": \"Nvidia\", \"Segment\": \"Compute\", \"Moat\": 5, \"Margin %\": 55, \"Growth %\": 45},\n",
        "    {\"Company\": \"Arista\", \"Segment\": \"Networking\", \"Moat\": 4, \"Margin %\": 38, \"Growth %\": 30},\n",
        "    {\"Company\": \"Vertiv\", \"Segment\": \"Power\", \"Moat\": 4, \"Margin %\": 25, \"Growth %\": 25},\n",
        "    {\"Company\": \"Supermicro\", \"Segment\": \"Compute\", \"Moat\": 3, \"Margin %\": 11, \"Growth %\": 40},\n",
        "]\n",
        "df = pd.DataFrame(data)\n",
        "\n",
        "# 3. Sidebar Filtering & Profitability Check\n",
        "df = df[df['Margin %'] > 0] # Filter out unprofitable companies\n",
        "\n",
        "# 4. Scoring Logic Function\n",
        "def get_margin_score(m):\n",
        "    if m > 40: return 5\n",
        "    elif m >= 30: return 4\n",
        "    elif m >= 20: return 3\n",
        "    elif m >= 10: return 2\n",
        "    else: return 1\n",
        "\n",
        "# 5. Interactive Table\n",
        "st.subheader(\"Interactive Research Table\")\n",
        "edited_df = st.data_editor(df, num_rows=\"dynamic\")\n",
        "\n",
        "# 6. Final Calculations\n",
        "edited_df['Margin Score'] = edited_df['Margin %'].apply(get_margin_score)\n",
        "edited_df['TAFGS'] = (edited_df['Moat'] * edited_df['Margin Score']) * edited_df['Growth %']\n",
        "final_df = edited_df.sort_values(\"TAFGS\", ascending=False)\n",
        "\n",
        "# 7. Dashboard Metrics & Charts\n",
        "top_segment = final_df.groupby(\"Segment\")[\"TAFGS\"].mean().idxmax()\n",
        "st.metric(\"Top Performing Segment\", top_segment)\n",
        "\n",
        "st.bar_chart(final_df.set_index(\"Company\")[\"TAFGS\"])\n",
        "\n",
        "# 8. Export Feature\n",
        "csv = final_df.to_csv(index=False).encode('utf-8')\n",
        "st.download_button(\"📥 Download Rankings\", data=csv, file_name='ai_rankings.csv')"
      ]
    }
  ]
}